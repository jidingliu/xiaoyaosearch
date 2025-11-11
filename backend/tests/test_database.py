"""
数据库测试
"""

import pytest
import tempfile
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.models.user import User
from app.models.file import File
from app.models.directory import Directory
from app.models.search_history import SearchHistory


class TestDatabase:
    """数据库测试类"""

    @pytest.fixture
    def temp_db(self):
        """临时数据库"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_file.close()

        engine = create_engine(f"sqlite:///{temp_file.name}")
        Base.metadata.create_all(bind=engine)

        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        yield SessionLocal

        os.unlink(temp_file.name)

    def test_create_user(self, temp_db):
        """测试创建用户"""
        db = temp_db()

        user = User(
            id="test_user_id",
            username="测试用户",
            email="test@example.com"
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        assert user.id == "test_user_id"
        assert user.username == "测试用户"
        assert user.email == "test@example.com"
        assert user.is_active is True

        db.close()

    def test_create_directory(self, temp_db):
        """测试创建目录"""
        db = temp_db()

        # 先创建用户
        user = User(id="user_id", username="用户")
        db.add(user)
        db.commit()

        # 创建目录
        directory = Directory(
            id="dir_id",
            user_id="user_id",
            path="/test/path",
            name="测试目录",
            status="active"
        )

        db.add(directory)
        db.commit()
        db.refresh(directory)

        assert directory.id == "dir_id"
        assert directory.user_id == "user_id"
        assert directory.path == "/test/path"
        assert directory.name == "测试目录"
        assert directory.status == "active"

        db.close()

    def test_create_file(self, temp_db):
        """测试创建文件"""
        db = temp_db()

        # 先创建用户和目录
        user = User(id="user_id", username="用户")
        db.add(user)

        directory = Directory(id="dir_id", user_id="user_id", path="/test", name="测试目录")
        db.add(directory)
        db.commit()

        # 创建文件
        file = File(
            id="file_id",
            user_id="user_id",
            directory_id="dir_id",
            file_name="测试文档.pdf",
            file_path="/test/测试文档.pdf",
            size=1024000,
            file_type="pdf",
            mime_type="application/pdf"
        )

        db.add(file)
        db.commit()
        db.refresh(file)

        assert file.id == "file_id"
        assert file.user_id == "user_id"
        assert file.directory_id == "dir_id"
        assert file.file_name == "测试文档.pdf"
        assert file.file_type == "pdf"
        assert file.size == 1024000

        db.close()

    def test_create_search_history(self, temp_db):
        """测试创建搜索历史"""
        db = temp_db()

        # 先创建用户
        user = User(id="user_id", username="用户")
        db.add(user)
        db.commit()

        # 创建搜索历史
        search_history = SearchHistory(
            id="search_id",
            user_id="user_id",
            query="机器学习",
            query_type="text",
            result_count=10,
            search_time=0.5
        )

        db.add(search_history)
        db.commit()
        db.refresh(search_history)

        assert search_history.id == "search_id"
        assert search_history.user_id == "user_id"
        assert search_history.query == "机器学习"
        assert search_history.query_type == "text"
        assert search_history.result_count == 10
        assert search_history.search_time == 0.5

        db.close()

    def test_relationships(self, temp_db):
        """测试关系"""
        db = temp_db()

        # 创建用户
        user = User(id="user_id", username="用户")
        db.add(user)
        db.commit()

        # 创建目录
        directory = Directory(id="dir_id", user_id="user_id", path="/test", name="测试目录")
        db.add(directory)
        db.commit()

        # 创建文件
        file = File(
            id="file_id",
            user_id="user_id",
            directory_id="dir_id",
            file_name="文档.pdf",
            file_path="/test/文档.pdf",
            size=1000000,
            file_type="pdf"
        )
        db.add(file)
        db.commit()

        # 创建搜索历史
        search_history = SearchHistory(
            id="search_id",
            user_id="user_id",
            query="搜索词",
            result_count=5
        )
        db.add(search_history)
        db.commit()

        # 测试关系
        # 用户关系
        assert len(user.directories) == 1
        assert len(user.files) == 1
        assert len(user.search_histories) == 1
        assert user.directories[0].id == "dir_id"
        assert user.files[0].id == "file_id"
        assert user.search_histories[0].id == "search_id"

        # 目录关系
        assert directory.user.id == "user_id"
        assert len(directory.files) == 1
        assert directory.files[0].id == "file_id"

        # 文件关系
        assert file.user.id == "user_id"
        assert file.directory.id == "dir_id"

        db.close()


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])