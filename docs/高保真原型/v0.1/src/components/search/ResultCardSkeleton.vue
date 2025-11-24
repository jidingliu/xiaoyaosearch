<template>
  <div class="result-card-skeleton">
    <div class="skeleton-header">
      <div class="skeleton-file-info">
        <div class="skeleton-file-icon">
          <div class="skeleton-shimmer"></div>
        </div>
        <div class="skeleton-file-details">
          <div class="skeleton-file-name">
            <div class="skeleton-shimmer"></div>
          </div>
          <div class="skeleton-file-meta">
            <div class="skeleton-shimmer meta-shimmer"></div>
            <div class="skeleton-shimmer meta-shimmer"></div>
            <div class="skeleton-shimmer meta-shimmer"></div>
          </div>
        </div>
      </div>
      <div class="skeleton-score">
        <div class="skeleton-score-circle">
          <div class="skeleton-shimmer"></div>
        </div>
        <div class="skeleton-score-label">
          <div class="skeleton-shimmer"></div>
        </div>
      </div>
    </div>

    <div class="skeleton-content">
      <div class="skeleton-preview-text">
        <div class="skeleton-shimmer line-shimmer"></div>
        <div class="skeleton-shimmer line-shimmer"></div>
        <div class="skeleton-shimmer line-shimmer short"></div>
      </div>
    </div>

    <div class="skeleton-footer">
      <div class="skeleton-match-type">
        <div class="skeleton-shimmer tag-shimmer"></div>
      </div>
      <div class="skeleton-actions">
        <div class="skeleton-shimmer action-shimmer"></div>
        <div class="skeleton-shimmer action-shimmer"></div>
        <div class="skeleton-shimmer action-shimmer"></div>
        <div class="skeleton-shimmer action-shimmer"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 骨架屏组件，不需要逻辑
</script>

<style lang="scss" scoped>
.result-card-skeleton {
  background: var(--surface-secondary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  position: relative;
  overflow: hidden;

  @include glass-morphism;
}

// 基础骨架屏样式
.skeleton-shimmer {
  background: linear-gradient(
    90deg,
    var(--surface-tertiary) 25%,
    var(--border-light) 50%,
    var(--surface-tertiary) 75%
  );
  background-size: 200% 100%;
  border-radius: var(--radius-sm);
  animation: shimmer-loading 1.5s ease-in-out infinite;

  @keyframes shimmer-loading {
    0% {
      background-position: -200% 0;
    }
    100% {
      background-position: 200% 0;
    }
  }
}

// 骨架屏头部
.skeleton-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-4);
}

.skeleton-file-info {
  display: flex;
  gap: var(--space-3);
  flex: 1;
}

.skeleton-file-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-lg);
  flex-shrink: 0;

  .skeleton-shimmer {
    width: 100%;
    height: 100%;
  }
}

.skeleton-file-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.skeleton-file-name {
  height: 22px;
  width: 70%;
  border-radius: var(--radius-sm);
}

.skeleton-file-meta {
  display: flex;
  gap: var(--space-2);
  align-items: center;
}

.meta-shimmer {
  height: 14px;
  width: 60px;
  border-radius: var(--radius-sm);

  &:nth-child(2) {
    width: 40px;
  }

  &:nth-child(3) {
    width: 50px;
  }
}

.skeleton-score {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-1);
  flex-shrink: 0;
}

.skeleton-score-circle {
  width: 50px;
  height: 50px;
  border-radius: 50%;

  .skeleton-shimmer {
    width: 100%;
    height: 100%;
  }
}

.skeleton-score-label {
  height: 14px;
  width: 40px;
  border-radius: var(--radius-sm);
}

// 骨架屏内容
.skeleton-content {
  margin-bottom: var(--space-4);
}

.skeleton-preview-text {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.line-shimmer {
  height: 16px;
  border-radius: var(--radius-sm);

  &:nth-child(1) {
    width: 90%;
  }

  &:nth-child(2) {
    width: 85%;
  }

  &.short {
    width: 60%;
  }
}

// 骨架屏底部
.skeleton-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: var(--space-3);
  border-top: 1px solid var(--border-light);
}

.skeleton-match-type {
  .tag-shimmer {
    height: 20px;
    width: 60px;
    border-radius: var(--radius-sm);
  }
}

.skeleton-actions {
  display: flex;
  gap: var(--space-1);
}

.action-shimmer {
  height: 28px;
  width: 32px;
  border-radius: var(--radius-sm);
}

// 脉冲动画效果
.skeleton-pulse {
  animation: skeleton-pulse 2s ease-in-out infinite;

  @keyframes skeleton-pulse {
    0%, 100% {
      opacity: 0.3;
    }
    50% {
      opacity: 0.8;
    }
  }
}

// 渐进式加载动画
.result-card-skeleton {
  animation: skeleton-fade-in 0.6s ease-out backwards;

  @keyframes skeleton-fade-in {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
}

// 多个骨架屏的交错动画
.result-card-skeleton:nth-child(1) { animation-delay: 0.1s; }
.result-card-skeleton:nth-child(2) { animation-delay: 0.2s; }
.result-card-skeleton:nth-child(3) { animation-delay: 0.3s; }
.result-card-skeleton:nth-child(4) { animation-delay: 0.4s; }
.result-card-skeleton:nth-child(5) { animation-delay: 0.5s; }
.result-card-skeleton:nth-child(6) { animation-delay: 0.6s; }

// 响应式设计
@media (max-width: 768px) {
  .result-card-skeleton {
    padding: var(--space-4);
  }

  .skeleton-header {
    flex-direction: column;
    gap: var(--space-3);
    align-items: stretch;
  }

  .skeleton-file-info {
    gap: var(--space-2);
  }

  .skeleton-file-icon {
    width: 32px;
    height: 32px;
  }

  .skeleton-file-name {
    height: 20px;
    width: 80%;
  }

  .skeleton-score {
    align-self: center;
  }

  .skeleton-score-circle {
    width: 40px;
    height: 40px;
  }

  .skeleton-footer {
    flex-direction: column;
    gap: var(--space-2);
    align-items: stretch;
  }

  .skeleton-actions {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .result-card-skeleton {
    padding: var(--space-3);
  }

  .skeleton-file-icon {
    width: 28px;
    height: 28px;
  }

  .skeleton-file-name {
    height: 18px;
    width: 90%;
  }

  .meta-shimmer {
    height: 12px;
    width: 50px;

    &:nth-child(2) {
      width: 35px;
    }

    &:nth-child(3) {
      width: 45px;
    }
  }

  .skeleton-score-circle {
    width: 36px;
    height: 36px;
  }

  .line-shimmer {
    height: 14px;

    &:nth-child(1) {
      width: 95%;
    }

    &:nth-child(2) {
      width: 88%;
    }

    &.short {
      width: 65%;
    }
  }

  .action-shimmer {
    height: 24px;
    width: 28px;
  }
}

// 无障碍
@media (prefers-reduced-motion: reduce) {
  .skeleton-shimmer {
    animation: none;
    background: var(--border-light);
  }

  .result-card-skeleton {
    animation: none;
  }
}

// 高对比度模式
@media (prefers-contrast: high) {
  .skeleton-shimmer {
    background: var(--border-heavy);
    animation: none;
  }

  .result-card-skeleton {
    border-color: var(--border-heavy);
  }
}

// 深色主题优化
[data-theme="dark"] {
  .skeleton-shimmer {
    background: linear-gradient(
      90deg,
      rgba(255, 255, 255, 0.05) 25%,
      rgba(255, 255, 255, 0.1) 50%,
      rgba(255, 255, 255, 0.05) 75%
    );
  }
}

// 浅色主题优化
[data-theme="light"] {
  .skeleton-shimmer {
    background: linear-gradient(
      90deg,
      rgba(0, 0, 0, 0.05) 25%,
      rgba(0, 0, 0, 0.1) 50%,
      rgba(0, 0, 0, 0.05) 75%
    );
  }
}
</style>