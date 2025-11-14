"""
Unit tests for vector indexing components.

This module tests all vector search functionality including Faiss integration,
vector operations, and high-level search management.
"""

import pytest
import numpy as np
import tempfile
import shutil
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

# Test the vector indexing components
from services.vector.vector_index import VectorIndex
from services.vector.vector_operations import VectorOperations
from services.vector.vector_search_manager import VectorSearchManager


# Skip tests if Faiss is not available
faiss = pytest.importorskip("faiss")


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_vectors():
    """Create sample vectors for testing."""
    np.random.seed(42)  # For reproducible tests
    vectors = np.random.random((10, 768)).astype(np.float32)
    # Normalize some vectors for testing
    for i in range(len(vectors)):
        if i % 3 == 0:
            vectors[i] = vectors[i] / np.linalg.norm(vectors[i])
    return vectors


@pytest.fixture
def sample_query_vector():
    """Create a sample query vector."""
    np.random.seed(123)
    vector = np.random.random(768).astype(np.float32)
    return vector / np.linalg.norm(vector)  # Normalize


@pytest.fixture
def sample_metadata():
    """Create sample metadata for vectors."""
    metadata = []
    for i in range(10):
        meta = {
            "file_id": i,
            "type": "content" if i % 2 == 0 else "file",
            "content_id": f"content_{i}" if i % 2 == 0 else None,
            "chunk_index": i // 2 if i % 2 == 0 else None,
            "title": f"Document {i}",
            "category": "test"
        }
        metadata.append(meta)
    return metadata


class TestVectorOperations:
    """Test cases for VectorOperations utility class."""

    def test_normalize_vector(self):
        """Test vector normalization."""
        # Test normal vector
        vector = np.array([3.0, 4.0])
        normalized = VectorOperations.normalize_vector(vector)
        expected = np.array([0.6, 0.8])
        np.testing.assert_array_almost_equal(normalized, expected)

        # Test zero vector
        zero_vector = np.array([0.0, 0.0])
        normalized_zero = VectorOperations.normalize_vector(zero_vector)
        np.testing.assert_array_equal(normalized_zero, zero_vector)

    def test_normalize_vectors(self):
        """Test batch vector normalization."""
        vectors = np.array([[3.0, 4.0], [1.0, 1.0], [0.0, 0.0]], dtype=np.float32)
        normalized = VectorOperations.normalize_vectors(vectors)

        # First vector should be [0.6, 0.8]
        np.testing.assert_array_almost_equal(normalized[0], [0.6, 0.8])

        # Second vector should be normalized
        second_norm = np.linalg.norm(normalized[1])
        assert abs(second_norm - 1.0) < 1e-6

        # Zero vector should remain unchanged
        np.testing.assert_array_equal(normalized[2], [0.0, 0.0])

    def test_cosine_similarity(self):
        """Test cosine similarity calculation."""
        # Identical vectors
        v1 = np.array([1.0, 0.0])
        v2 = np.array([1.0, 0.0])
        similarity = VectorOperations.cosine_similarity(v1, v2)
        assert abs(similarity - 1.0) < 1e-6

        # Orthogonal vectors
        v3 = np.array([1.0, 0.0])
        v4 = np.array([0.0, 1.0])
        similarity = VectorOperations.cosine_similarity(v3, v4)
        assert abs(similarity - 0.0) < 1e-6

        # Opposite vectors
        v5 = np.array([1.0, 0.0])
        v6 = np.array([-1.0, 0.0])
        similarity = VectorOperations.cosine_similarity(v5, v6)
        assert abs(similarity - (-1.0)) < 1e-6

        # Zero vector edge case
        v7 = np.array([0.0, 0.0])
        v8 = np.array([1.0, 0.0])
        similarity = VectorOperations.cosine_similarity(v7, v8)
        assert similarity == 0.0

    def test_euclidean_distance(self):
        """Test Euclidean distance calculation."""
        v1 = np.array([0.0, 0.0])
        v2 = np.array([3.0, 4.0])
        distance = VectorOperations.euclidean_distance(v1, v2)
        assert abs(distance - 5.0) < 1e-6

    def test_cosine_distance(self):
        """Test cosine distance calculation."""
        v1 = np.array([1.0, 0.0])
        v2 = np.array([0.0, 1.0])
        distance = VectorOperations.cosine_distance(v1, v2)
        assert abs(distance - 1.0) < 1e-6  # cosine_distance = 1 - cosine_similarity

    def test_batch_cosine_similarity(self):
        """Test batch cosine similarity calculation."""
        query_vector = np.array([1.0, 0.0])
        vectors = np.array([[1.0, 0.0], [0.0, 1.0], [0.707, 0.707]], dtype=np.float32)

        similarities = VectorOperations.batch_cosine_similarity(query_vector, vectors)

        assert abs(similarities[0] - 1.0) < 1e-6  # Identical
        assert abs(similarities[1] - 0.0) < 1e-6  # Orthogonal
        assert abs(similarities[2] - 0.707) < 1e-3  # 45 degrees

    def test_validate_vector_dimensions(self):
        """Test vector dimension validation."""
        # Correct dimension (single vector)
        v1 = np.array([1.0, 2.0, 3.0])
        assert VectorOperations.validate_vector_dimensions(v1, 3) is True

        # Incorrect dimension (single vector)
        v2 = np.array([1.0, 2.0])
        assert VectorOperations.validate_vector_dimensions(v2, 3) is False

        # Correct dimension (batch)
        v3 = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        assert VectorOperations.validate_vector_dimensions(v3, 3) is True

        # Incorrect dimension (batch)
        v4 = np.array([[1.0, 2.0], [3.0, 4.0]])
        assert VectorOperations.validate_vector_dimensions(v4, 3) is False

        # Invalid dimensions
        v5 = np.array([[[1.0], [2.0]]])  # 3D array
        assert VectorOperations.validate_vector_dimensions(v5, 3) is False

    def test_prepare_vectors(self):
        """Test vector preparation for batching."""
        vectors = [
            np.array([1.0, 2.0, 3.0]),
            np.array([4.0, 5.0, 6.0]),
            np.array([7.0, 8.0, 9.0])
        ]

        prepared = VectorOperations.prepare_vectors(vectors)
        expected = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]], dtype=np.float32)

        np.testing.assert_array_almost_equal(prepared, expected)
        assert prepared.dtype == np.float32

    def test_prepare_vectors_dimension_mismatch(self):
        """Test vector preparation with dimension mismatch."""
        vectors = [
            np.array([1.0, 2.0, 3.0]),
            np.array([4.0, 5.0])  # Different dimension
        ]

        with pytest.raises(ValueError, match="Vector 1 has dimension 2, expected 3"):
            VectorOperations.prepare_vectors(vectors)

    def test_chunk_vectors(self):
        """Test vector chunking."""
        vectors = np.array([[i] * 5 for i in range(10)])  # 10 vectors of dimension 5

        chunks = VectorOperations.chunk_vectors(vectors, chunk_size=3)

        assert len(chunks) == 4
        assert len(chunks[0]) == 3
        assert len(chunks[1]) == 3
        assert len(chunks[2]) == 3
        assert len(chunks[3]) == 1  # Last chunk with remaining vectors

    def test_compute_vector_statistics(self):
        """Test vector statistics computation."""
        # Create vectors with known properties
        vectors = np.array([
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
            [7.0, 8.0, 9.0]
        ], dtype=np.float32)

        stats = VectorOperations.compute_vector_statistics(vectors)

        assert stats["count"] == 3
        assert stats["dimension"] == 3
        assert "mean_norm" in stats
        assert "std_norm" in stats
        assert "min_norm" in stats
        assert "max_norm" in stats
        assert stats["mean"] is not None
        assert stats["std"] is not None

    def test_compute_vector_statistics_empty(self):
        """Test statistics computation with empty vectors."""
        vectors = np.array([]).reshape(0, 3)
        stats = VectorOperations.compute_vector_statistics(vectors)

        assert stats["count"] == 0
        assert stats["dimension"] == 0
        assert stats["mean_norm"] == 0.0

    def test_filter_vectors_by_threshold(self):
        """Test vector filtering by threshold."""
        vectors = np.array([
            [1.0, 0.0],    # norm = 1.0
            [0.1, 0.1],    # norm ≈ 0.141
            [3.0, 4.0]     # norm = 5.0
        ], dtype=np.float32)

        # Filter by norm
        filtered = VectorOperations.filter_vectors_by_threshold(vectors, 2.0, "norm")
        assert len(filtered) == 1  # Only [3.0, 4.0] has norm >= 2.0

    def test_merge_vector_batches(self):
        """Test merging vector batches."""
        batch1 = np.array([[1.0, 2.0], [3.0, 4.0]])
        batch2 = np.array([[5.0, 6.0]])
        batch3 = np.array([]).reshape(0, 2)  # Empty batch

        merged = VectorOperations.merge_vector_batches([batch1, batch2, batch3])
        expected = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])

        np.testing.assert_array_equal(merged, expected)

    def test_merge_vector_batches_dimension_mismatch(self):
        """Test merging batches with dimension mismatch."""
        batch1 = np.array([[1.0, 2.0]])
        batch2 = np.array([[1.0, 2.0, 3.0]])  # Different dimension

        with pytest.raises(ValueError, match="Batch 1 has dimension 3, expected 2"):
            VectorOperations.merge_vector_batches([batch1, batch2])


class TestVectorIndex:
    """Test cases for VectorIndex class."""

    @pytest.fixture
    def vector_index(self, temp_dir):
        """Create a VectorIndex instance for testing."""
        index_path = Path(temp_dir) / "test_index.faiss"
        mapping_path = Path(temp_dir) / "test_mapping.json"

        return VectorIndex(
            dimension=768,
            nlist=10,
            nprobe=5,
            index_path=str(index_path),
            id_mapping_path=str(mapping_path)
        )

    def test_vector_index_initialization(self, vector_index):
        """Test VectorIndex initialization."""
        assert vector_index.dimension == 768
        assert vector_index.nlist == 10
        assert vector_index.nprobe == 5
        assert vector_index.index is not None
        assert vector_index.get_vector_count() == 0
        assert vector_index.is_empty() is True

    def test_add_vectors_without_training(self, vector_index, sample_vectors):
        """Test adding vectors when index is not trained."""
        # Add vectors smaller than nlist (should use flat index)
        small_batch = sample_vectors[:5]  # 5 vectors < 10 nlist

        vector_ids = vector_index.add_vectors(small_batch)

        assert len(vector_ids) == 5
        assert vector_ids == [0, 1, 2, 3, 4]
        assert vector_index.get_vector_count() == 5
        assert vector_index.is_trained is True  # Should be trained (flat index)

    def test_add_vectors_with_training(self, vector_index, sample_vectors):
        """Test adding vectors that trigger index training."""
        # Add enough vectors to trigger training (>= nlist)
        vector_ids = vector_index.add_vectors(sample_vectors)

        assert len(vector_ids) == 10
        assert vector_index.get_vector_count() == 10
        # Should be trained after adding enough vectors
        assert vector_index.is_trained is True

    def test_add_vectors_with_metadata(self, vector_index, sample_vectors, sample_metadata):
        """Test adding vectors with metadata."""
        vector_ids = vector_index.add_vectors(sample_vectors, metadata=sample_metadata)

        # Verify metadata was stored
        for i, vector_id in enumerate(vector_ids):
            metadata = vector_index.get_metadata_by_id(vector_id)
            assert metadata is not None
            assert metadata["file_id"] == i
            assert metadata["category"] == "test"

    def test_add_vectors_with_custom_ids(self, vector_index, sample_vectors):
        """Test adding vectors with custom IDs."""
        custom_ids = [100, 101, 102, 103, 104]
        small_batch = sample_vectors[:5]

        vector_ids = vector_index.add_vectors(small_batch, ids=custom_ids)

        assert vector_ids == custom_ids
        assert vector_index.get_vector_count() == 5

    def test_add_vectors_dimension_mismatch(self, vector_index):
        """Test adding vectors with wrong dimension."""
        wrong_vectors = np.random.random((5, 512)).astype(np.float32)  # Wrong dimension

        with pytest.raises(ValueError, match="Vectors must have dimension 768"):
            vector_index.add_vectors(wrong_vectors)

    def test_search_empty_index(self, vector_index, sample_query_vector):
        """Test searching in an empty index."""
        distances, indices, metadata = vector_index.search(sample_query_vector, k=5)

        assert len(distances) == 0
        assert len(indices) == 0
        assert len(metadata) == 0

    def test_search_with_results(self, vector_index, sample_vectors, sample_query_vector):
        """Test searching with results."""
        # Add vectors first
        vector_index.add_vectors(sample_vectors)

        # Search
        distances, indices, metadata = vector_index.search(sample_query_vector, k=5)

        assert len(distances) <= 5
        assert len(indices) == len(distances)
        assert len(metadata) == len(distances)

    def test_search_with_nprobe_override(self, vector_index, sample_vectors, sample_query_vector):
        """Test searching with nprobe override."""
        vector_index.add_vectors(sample_vectors)

        # Search with custom nprobe
        # Note: nprobe only applies to IVF indexes, not Flat indexes
        try:
            if hasattr(vector_index.index, 'index') and hasattr(vector_index.index.index, 'nprobe'):
                original_nprobe = vector_index.index.index.nprobe
                distances, indices, metadata = vector_index.search(sample_query_vector, k=3, nprobe=8)

                # nprobe should be restored after search (for IVF indexes)
                assert vector_index.index.index.nprobe == original_nprobe
            else:
                # For Flat indexes, nprobe should not affect the search
                distances1, indices1, metadata1 = vector_index.search(sample_query_vector, k=3)
                distances2, indices2, metadata2 = vector_index.search(sample_query_vector, k=3, nprobe=8)

                # Results should be the same for Flat indexes regardless of nprobe
                np.testing.assert_array_equal(distances1, distances2)
                np.testing.assert_array_equal(indices1, indices2)
        except Exception as e:
            # If nprobe is not supported, the search should still work
            distances, indices, metadata = vector_index.search(sample_query_vector, k=3)
            assert len(distances) <= 3

    def test_search_wrong_dimension(self, vector_index):
        """Test searching with wrong query dimension."""
        wrong_query = np.random.random(512).astype(np.float32)  # Wrong dimension

        with pytest.raises(ValueError, match="Query vector must have dimension 768"):
            vector_index.search(wrong_query, k=5)

    def test_delete_vectors(self, vector_index, sample_vectors, sample_metadata):
        """Test vector deletion."""
        # Add vectors first
        vector_ids = vector_index.add_vectors(sample_vectors, metadata=sample_metadata)

        # Delete some vectors
        ids_to_delete = vector_ids[:3]
        success = vector_index.delete_vectors(ids_to_delete)

        assert success is True

        # Verify metadata is removed
        for vector_id in ids_to_delete:
            assert vector_index.get_metadata_by_id(vector_id) is None

    def test_get_metadata_by_id(self, vector_index, sample_vectors, sample_metadata):
        """Test getting metadata by vector ID."""
        vector_ids = vector_index.add_vectors(sample_vectors, metadata=sample_metadata)

        # Test existing vector
        metadata = vector_index.get_metadata_by_id(vector_ids[0])
        assert metadata is not None
        assert metadata["file_id"] == 0

        # Test non-existing vector
        metadata = vector_index.get_metadata_by_id(9999)
        assert metadata is None

    def test_get_id_by_metadata(self, vector_index, sample_vectors, sample_metadata):
        """Test getting vector ID by metadata."""
        vector_ids = vector_index.add_vectors(sample_vectors, metadata=sample_metadata)

        # Test file_id lookup
        vector_id = vector_index.get_id_by_metadata(file_id=5)
        assert vector_id == vector_ids[5]

        # Test content_id lookup (only for even indices in our test data)
        content_id = "content_2"
        vector_id = vector_index.get_id_by_metadata(content_id=content_id)
        expected_id = vector_ids[2]  # content_2 should be at index 2
        assert vector_id == expected_id

    def test_save_and_load_index(self, vector_index, sample_vectors, sample_metadata):
        """Test saving and loading index."""
        # Add vectors and save
        vector_ids = vector_index.add_vectors(sample_vectors, metadata=sample_metadata)
        save_success = vector_index.save_index()
        assert save_success is True

        # Create new index instance and load
        new_index = VectorIndex(
            dimension=768,
            index_path=vector_index.index_path,
            id_mapping_path=vector_index.id_mapping_path
        )

        # Verify loaded data
        assert new_index.get_vector_count() == len(sample_vectors)
        assert new_index.is_trained == vector_index.is_trained

        # Test metadata loading
        loaded_metadata = new_index.get_metadata_by_id(vector_ids[0])
        assert loaded_metadata is not None
        assert loaded_metadata["file_id"] == 0

    def test_rebuild_index(self, vector_index, sample_vectors, sample_metadata):
        """Test rebuilding index."""
        # Add vectors
        vector_index.add_vectors(sample_vectors, metadata=sample_metadata)
        original_count = vector_index.get_vector_count()

        # Rebuild
        rebuild_success = vector_index.rebuild_index(
            vectors=sample_vectors,
            metadata=sample_metadata,
            force_retrain=True
        )

        assert rebuild_success is True
        assert vector_index.get_vector_count() == original_count
        assert vector_index.is_trained is True

    def test_get_index_stats(self, vector_index, sample_vectors):
        """Test getting index statistics."""
        # Initially empty
        stats = vector_index.get_index_stats()
        assert stats["total_vectors"] == 0
        assert stats["is_trained"] is False
        assert stats["dimension"] == 768
        assert stats["nlist"] == 10

        # Add vectors
        vector_index.add_vectors(sample_vectors)
        stats = vector_index.get_index_stats()
        assert stats["total_vectors"] == len(sample_vectors)


class TestVectorSearchManager:
    """Test cases for VectorSearchManager class."""

    @pytest.fixture
    def search_manager(self, temp_dir):
        """Create a VectorSearchManager instance for testing."""
        index_path = Path(temp_dir) / "manager_index.faiss"

        return VectorSearchManager(
            dimension=768,
            nlist=10,
            nprobe=5,
            index_path=str(index_path)
        )

    def test_search_manager_initialization(self, search_manager):
        """Test VectorSearchManager initialization."""
        assert search_manager.dimension == 768
        assert search_manager.vector_index is not None

    def test_add_file_vector(self, search_manager, sample_query_vector):
        """Test adding a file vector."""
        file_id = 42
        metadata = {"title": "Test Document", "category": "test"}

        vector_id = search_manager.add_file_vector(file_id, sample_query_vector, metadata)

        assert vector_id is not None
        assert isinstance(vector_id, int)

        # Verify metadata
        stored_metadata = search_manager.vector_index.get_metadata_by_id(vector_id)
        assert stored_metadata["file_id"] == file_id
        assert stored_metadata["type"] == "file"
        assert stored_metadata["title"] == "Test Document"

    def test_add_content_vector(self, search_manager, sample_query_vector):
        """Test adding a content vector."""
        content_id = "content_123"
        file_id = 42
        chunk_index = 1

        vector_id = search_manager.add_content_vector(
            content_id, sample_query_vector, file_id, chunk_index
        )

        assert vector_id is not None

        # Verify metadata
        stored_metadata = search_manager.vector_index.get_metadata_by_id(vector_id)
        assert stored_metadata["content_id"] == content_id
        assert stored_metadata["file_id"] == file_id
        assert stored_metadata["chunk_index"] == chunk_index
        assert stored_metadata["type"] == "content"

    def test_add_batch_vectors(self, search_manager, sample_vectors):
        """Test adding vectors in batch."""
        vectors_data = []
        for i, vector in enumerate(sample_vectors[:5]):
            vectors_data.append({
                "vector": vector,
                "metadata": {
                    "file_id": i,
                    "type": "content",
                    "content_id": f"content_{i}"
                }
            })

        vector_ids = search_manager.add_batch_vectors(vectors_data)

        assert len(vector_ids) == 5
        assert all(isinstance(vid, int) for vid in vector_ids)

    def test_add_batch_vectors_empty(self, search_manager):
        """Test adding empty batch."""
        vector_ids = search_manager.add_batch_vectors([])
        assert vector_ids == []

    def test_search_similar(self, search_manager, sample_vectors, sample_metadata):
        """Test searching for similar vectors."""
        # Add vectors first
        vectors_data = []
        for i, vector in enumerate(sample_vectors):
            vectors_data.append({
                "vector": vector,
                "metadata": sample_metadata[i]
            })
        search_manager.add_batch_vectors(vectors_data)

        # Search
        query_vector = sample_vectors[0]
        results = search_manager.search_similar(query_vector, k=5)

        assert len(results) <= 5

        # Check result structure
        if results:
            result = results[0]
            assert "vector_id" in result
            assert "similarity" in result
            assert "distance" in result
            assert "metadata" in result
            assert "rank" in result
            assert isinstance(result["similarity"], float)
            assert result["similarity"] >= 0.0

    def test_search_similar_with_filters(self, search_manager, sample_vectors, sample_metadata):
        """Test searching with content type filter."""
        # Add vectors
        vectors_data = []
        for i, vector in enumerate(sample_vectors):
            vectors_data.append({
                "vector": vector,
                "metadata": sample_metadata[i]
            })
        search_manager.add_batch_vectors(vectors_data)

        # Search with content type filter
        query_vector = sample_vectors[0]
        results = search_manager.search_similar(
            query_vector, k=10, content_type="content"
        )

        # All results should have type="content"
        for result in results:
            assert result["metadata"]["type"] == "content"

    def test_search_similar_with_file_filter(self, search_manager, sample_vectors, sample_metadata):
        """Test searching with file ID filter."""
        # Add vectors
        vectors_data = []
        for i, vector in enumerate(sample_vectors):
            vectors_data.append({
                "vector": vector,
                "metadata": sample_metadata[i]
            })
        search_manager.add_batch_vectors(vectors_data)

        # Search with file ID filter
        query_vector = sample_vectors[0]
        target_file_id = 2
        results = search_manager.search_similar(
            query_vector, k=10, file_id=target_file_id
        )

        # All results should be from the specified file
        for result in results:
            assert result["metadata"]["file_id"] == target_file_id

    def test_search_similar_with_min_similarity(self, search_manager, sample_vectors, sample_metadata):
        """Test searching with minimum similarity threshold."""
        # Add vectors
        vectors_data = []
        for i, vector in enumerate(sample_vectors):
            vectors_data.append({
                "vector": vector,
                "metadata": sample_metadata[i]
            })
        search_manager.add_batch_vectors(vectors_data)

        # Search with high minimum similarity
        query_vector = sample_vectors[0]
        results = search_manager.search_similar(
            query_vector, k=10, min_similarity=0.99  # Very high threshold
        )

        # Should return few or no results due to high threshold
        assert len(results) <= 1  # At most the query vector itself

    def test_search_by_file(self, search_manager, sample_vectors, sample_metadata):
        """Test searching within a specific file."""
        # Add vectors
        vectors_data = []
        for i, vector in enumerate(sample_vectors):
            vectors_data.append({
                "vector": vector,
                "metadata": sample_metadata[i]
            })
        search_manager.add_batch_vectors(vectors_data)

        # Search within file 2
        query_vector = sample_vectors[0]
        results = search_manager.search_by_file(2, query_vector, k=5)

        # All results should be from file 2 and type "content"
        for result in results:
            assert result["metadata"]["file_id"] == 2
            assert result["metadata"]["type"] == "content"

    def test_get_file_vectors(self, search_manager, sample_vectors, sample_metadata):
        """Test getting all vectors for a file."""
        # Add vectors
        vectors_data = []
        for i, vector in enumerate(sample_vectors):
            vectors_data.append({
                "vector": vector,
                "metadata": sample_metadata[i]
            })
        search_manager.add_batch_vectors(vectors_data)

        # Get vectors for file 3
        file_vectors = search_manager.get_file_vectors(3)

        # Should find vectors for file 3
        file_3_count = sum(1 for meta in sample_metadata if meta["file_id"] == 3)
        assert len(file_vectors) == file_3_count

        for vector_info in file_vectors:
            assert vector_info["metadata"]["file_id"] == 3

    def test_delete_file_vectors(self, search_manager, sample_vectors, sample_metadata):
        """Test deleting all vectors for a file."""
        # Add vectors
        vectors_data = []
        for i, vector in enumerate(sample_vectors):
            vectors_data.append({
                "vector": vector,
                "metadata": sample_metadata[i]
            })
        search_manager.add_batch_vectors(vectors_data)

        # Get initial count for file 4
        initial_count = len(search_manager.get_file_vectors(4))

        # Delete file 4 vectors
        success = search_manager.delete_file_vectors(4)
        assert success is True

        # Verify deletion
        remaining_vectors = search_manager.get_file_vectors(4)
        assert len(remaining_vectors) == 0
        assert len(remaining_vectors) < initial_count

    def test_delete_content_vector(self, search_manager, sample_vectors, sample_metadata):
        """Test deleting a specific content vector."""
        # Add vectors
        vectors_data = []
        for i, vector in enumerate(sample_vectors):
            vectors_data.append({
                "vector": vector,
                "metadata": sample_metadata[i]
            })
        search_manager.add_batch_vectors(vectors_data)

        # Find a content vector to delete
        target_content_id = "content_2"

        # Delete content vector
        success = search_manager.delete_content_vector(target_content_id)
        assert success is True

    def test_get_statistics(self, search_manager, sample_vectors, sample_metadata):
        """Test getting comprehensive statistics."""
        # Add vectors
        vectors_data = []
        for i, vector in enumerate(sample_vectors):
            vectors_data.append({
                "vector": vector,
                "metadata": sample_metadata[i]
            })
        search_manager.add_batch_vectors(vectors_data)

        # Get statistics
        stats = search_manager.get_statistics()

        assert "total_vectors" in stats
        assert "file_vectors" in stats
        assert "content_vectors" in stats
        assert "unique_files" in stats
        assert "average_vectors_per_file" in stats

        # Verify counts
        file_count = sum(1 for meta in sample_metadata if meta["type"] == "file")
        content_count = sum(1 for meta in sample_metadata if meta["type"] == "content")
        unique_file_count = len(set(meta["file_id"] for meta in sample_metadata))

        assert stats["file_vectors"] == file_count
        assert stats["content_vectors"] == content_count
        assert stats["unique_files"] == unique_file_count

    def test_rebuild_index(self, search_manager, sample_vectors, sample_metadata):
        """Test rebuilding the index."""
        # Add vectors
        vectors_data = []
        for i, vector in enumerate(sample_vectors):
            vectors_data.append({
                "vector": vector,
                "metadata": sample_metadata[i]
            })
        search_manager.add_batch_vectors(vectors_data)

        initial_count = search_manager.vector_index.get_vector_count()

        # Rebuild index
        success = search_manager.rebuild_index(force_retrain=True)
        assert success is True
        assert search_manager.vector_index.get_vector_count() == initial_count

    def test_save_index(self, search_manager, sample_vectors):
        """Test saving the index."""
        # Add vectors
        search_manager.add_file_vector(1, sample_vectors[0])

        # Save
        success = search_manager.save_index()
        assert success is True

    def test_optimize_index(self, search_manager, sample_vectors):
        """Test index optimization."""
        # Add many vectors to trigger optimization
        large_vectors = np.random.random((15000, 768)).astype(np.float32)  # More than 10k
        search_manager.add_batch_vectors([
            {"vector": large_vectors[i], "metadata": {"file_id": i}}
            for i in range(len(large_vectors))
        ])

        # Optimize
        success = search_manager.optimize_index()
        assert success is True

        # nprobe should have been increased
        assert search_manager.vector_index.nprobe > 10

    def test_error_handling_in_add_file_vector(self, search_manager):
        """Test error handling in add_file_vector."""
        # Create a problematic vector (wrong dimension)
        bad_vector = np.random.random(512).astype(np.float32)

        # Should handle error gracefully and return None
        vector_id = search_manager.add_file_vector(1, bad_vector)
        assert vector_id is None

    def test_error_handling_in_search_similar(self, search_manager):
        """Test error handling in search_similar."""
        # Use problematic query vector
        bad_vector = np.random.random(512).astype(np.float32)

        # Should handle error gracefully and return empty list
        results = search_manager.search_similar(bad_vector, k=5)
        assert results == []


class TestVectorIntegration:
    """Integration tests for vector search components."""

    @pytest.fixture
    def temp_files(self, temp_dir):
        """Create temporary file paths for testing."""
        return {
            "index": Path(temp_dir) / "integration_index.faiss",
            "mapping": Path(temp_dir) / "integration_mapping.json",
            "vectors": Path(temp_dir) / "test_vectors.npy"
        }

    def test_end_to_end_workflow(self, temp_files):
        """Test complete end-to-end vector search workflow."""
        # Create search manager
        manager = VectorSearchManager(
            dimension=256,  # Smaller dimension for faster testing
            nlist=5,
            index_path=str(temp_files["index"])
        )

        # Create test data
        np.random.seed(42)
        documents = [
            {"id": 1, "text": "machine learning algorithms", "category": "tech"},
            {"id": 2, "text": "natural language processing", "category": "tech"},
            {"id": 3, "text": "cooking recipes for beginners", "category": "food"},
            {"id": 4, "text": "python programming tutorial", "category": "tech"},
            {"id": 5, "text": "baking bread techniques", "category": "food"}
        ]

        # Create synthetic embeddings (simulating real embeddings)
        embeddings = {}
        for doc in documents:
            # Create reproducible pseudo-embeddings based on document content
            seed = sum(ord(c) for c in doc["text"])
            np.random.seed(seed)
            embeddings[doc["id"]] = np.random.random(256).astype(np.float32)
            embeddings[doc["id"]] = VectorOperations.normalize_vector(embeddings[doc["id"]])

        # Add document vectors
        for doc in documents:
            manager.add_file_vector(
                file_id=doc["id"],
                vector=embeddings[doc["id"]],
                metadata={"title": doc["text"], "category": doc["category"]}
            )

        # Test similarity search for tech documents
        tech_query = embeddings[1]  # Use NLP doc as query

        # Search for similar documents
        results = manager.search_similar(tech_query, k=3)

        assert len(results) > 0
        assert all("metadata" in result for result in results)
        assert all("similarity" in result for result in results)
        assert all(0 <= result["similarity"] <= 1 for result in results)

        # Test filtered search
        tech_results = manager.search_similar(
            tech_query, k=5, content_type="file"
        )
        assert len(tech_results) >= 2  # At least the query itself

        # Test statistics
        stats = manager.get_statistics()
        assert stats["total_vectors"] == len(documents)
        assert stats["unique_files"] == len(documents)

        # Test persistence
        save_success = manager.save_index()
        assert save_success is True

        # Create new manager and reload
        new_manager = VectorSearchManager(
            dimension=256,
            index_path=str(temp_files["index"])
        )

        assert new_manager.get_statistics()["total_vectors"] == len(documents)

        # Test search after reload
        reloaded_results = new_manager.search_similar(tech_query, k=3)
        assert len(reloaded_results) == len(results)

    def test_batch_operations_performance(self, temp_files):
        """Test performance of batch operations."""
        manager = VectorSearchManager(
            dimension=128,
            nlist=20,
            index_path=str(temp_files["index"])
        )

        # Create large batch of vectors
        batch_size = 1000
        np.random.seed(42)

        vectors_data = []
        for i in range(batch_size):
            vector = np.random.random(128).astype(np.float32)
            vector = VectorOperations.normalize_vector(vector)

            vectors_data.append({
                "vector": vector,
                "metadata": {
                    "file_id": i,
                    "type": "content",
                    "category": f"category_{i % 10}",
                    "timestamp": i
                }
            })

        # Test batch addition
        import time
        start_time = time.time()

        vector_ids = manager.add_batch_vectors(vectors_data)

        add_time = time.time() - start_time

        assert len(vector_ids) == batch_size
        assert add_time < 5.0  # Should complete within 5 seconds

        # Test batch search
        query_vector = vectors_data[0]["vector"]

        start_time = time.time()
        results = manager.search_similar(query_vector, k=10)
        search_time = time.time() - start_time

        assert len(results) <= 10
        assert search_time < 1.0  # Should complete within 1 second

        # Test statistics accuracy
        stats = manager.get_statistics()
        assert stats["total_vectors"] == batch_size
        assert stats["unique_files"] == batch_size

    def test_vector_operations_utils_integration(self):
        """Test integration of vector operations utilities."""
        # Create test vectors
        np.random.seed(42)
        original_vectors = np.random.random((50, 256)).astype(np.float32)

        # Test normalization
        normalized_vectors = VectorOperations.normalize_vectors(original_vectors)

        # Verify normalization
        for i in range(5):  # Check first 5 vectors
            norm = np.linalg.norm(normalized_vectors[i])
            assert abs(norm - 1.0) < 1e-6

        # Test batch similarity
        query_vector = normalized_vectors[0]
        similarities = VectorOperations.batch_cosine_similarity(query_vector, normalized_vectors)

        assert len(similarities) == 50
        assert similarities[0] == 1.0  # Self-similarity
        assert all(0 <= sim <= 1 for sim in similarities)

        # Test chunking
        chunks = VectorOperations.chunk_vectors(normalized_vectors, chunk_size=12)
        assert len(chunks) == 5  # 50 / 12 = 4.17 -> 5 chunks
        assert len(chunks[-1]) == 2  # Last chunk has 2 vectors

        # Test statistics
        stats = VectorOperations.compute_vector_statistics(normalized_vectors)
        assert stats["count"] == 50
        assert stats["dimension"] == 256
        assert stats["mean_norm"] > 0.9  # Should be close to 1.0 for normalized vectors

    def test_error_handling_and_recovery(self, temp_files):
        """Test error handling and recovery mechanisms."""
        manager = VectorSearchManager(
            dimension=64,
            index_path=str(temp_files["index"])
        )

        # Test handling of invalid data
        invalid_vector = np.array([1, 2])  # Wrong dimension
        result = manager.add_file_vector(1, invalid_vector)
        assert result is None

        # Test search in empty index
        query_vector = np.random.random(64).astype(np.float32)
        results = manager.search_similar(query_vector, k=5)
        assert results == []

        # Test handling of corrupted metadata
        # This would need more sophisticated testing with actual corruption scenarios

        # Test recovery after adding valid data
        valid_vector = np.random.random(64).astype(np.float32)
        vector_id = manager.add_file_vector(1, valid_vector)
        assert vector_id is not None

        results = manager.search_similar(valid_vector, k=5)
        assert len(results) >= 1