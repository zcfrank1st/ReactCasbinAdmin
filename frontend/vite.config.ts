import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
// export default defineConfig({
//   plugins: [react()]
// })

export default ({ mode }) => {
  var target = ''
  if (mode === 'dev'){
    target = 'dist'
  } else if(mode === 'prod') {
    target = process.cwd().replace('frontend', 'backend/static/')
  }
  
  return defineConfig({
      plugins: [react()],
      build: {
        outDir: target
      }
  }); 
};


// import { defineConfig, loadEnv } from 'vite'

// export default defineConfig(({ command, mode }) => {
//   // 根据当前工作目录中的 `mode` 加载 .env 文件
//   // 设置第三个参数为 '' 来加载所有环境变量，而不管是否有 `VITE_` 前缀。
//   const env = loadEnv(mode, process.cwd(), '')
//   return {
//     // vite 配置
//     define: {
//       __APP_ENV__: env.APP_ENV
//     }
//   }
// })