<template>
  <router-view />
</template>

<script setup>
// 主应用入口，通过路由控制页面显示
</script>

<style>
/* 全局样式变量 */
:root {
  --primary-light: #5c9eff;
  --primary: #2b6ef0;
  --primary-dark: #0a58ca;
  --bg-sidebar: #ffffffd9;
  --bg-card: #ffffff;
  --shadow-sm: 0 4px 12px rgba(0, 82, 212, 0.08);
  --border-light: #d9e8ff;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', 'PingFang SC', Roboto, 'Helvetica Neue', sans-serif;
  background-color: #eef5ff;
  overflow-x: hidden;
}

/* 卡片样式 */
.card {
  background: var(--bg-card);
  border-radius: 24px;
  padding: 20px 24px;
  margin-bottom: 24px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-light);
  transition: 0.1s;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
  border-left: 4px solid var(--primary);
  padding-left: 14px;
}

.grid-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

/* 进度条样式 */
.progress-bar {
  width: 100%;
  height: 6px;
  background: #e2e8f0;
  border-radius: 10px;
  margin-top: 10px;
}

.progress-fill {
  width: 0%;
  height: 100%;
  background: var(--primary);
  border-radius: 10px;
  transition: width 0.3s;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .grid-2col {
    grid-template-columns: 1fr;
  }
}
</style>