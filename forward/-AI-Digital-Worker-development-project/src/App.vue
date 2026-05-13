<template>
  <router-view />
</template>

<script setup>
// 主应用入口，通过路由控制页面显示
</script>

<style>
/* 全局样式变量 */
:root {
  --primary-light: #8ab4f8;
  --primary: #2b6ef0;
  --primary-dark: #1a4bd6;
  --secondary: #10b981;
  --bg-sidebar: rgba(255, 255, 255, 0.95);
  --bg-card: #ffffff;
  --bg-body: #f8fafc;
  --shadow-sm: 0 2px 8px rgba(43, 110, 240, 0.06);
  --shadow-md: 0 8px 24px rgba(43, 110, 240, 0.12);
  --shadow-lg: 0 12px 40px rgba(43, 110, 240, 0.18);
  --border-light: #e2e8f0;
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --text-tertiary: #94a3b8;
  --radius-sm: 8px;
  --radius-md: 16px;
  --radius-lg: 24px;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', 'Segoe UI', 'PingFang SC', Roboto, 'Helvetica Neue', sans-serif;
  background-color: var(--bg-body);
  color: var(--text-primary);
  overflow-x: hidden;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* 卡片样式 */
.card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 24px 32px;
  margin-bottom: 24px;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-light);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
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