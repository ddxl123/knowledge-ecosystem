# Next.js

## Next.js基础概念
- Next.js：React的全栈框架，由Vercel开发，生产级应用首选
- 核心特性：SSR、SSG、ISR、API路由、文件系统路由、自动代码分割
- 创建项目：`npx create-next-app@latest my-app`
- 目录结构：app/（App Router，推荐）、pages/（Pages Router，传统）
- 启动开发：`npm run dev` 启动开发服务器

## App Router（推荐）
- 文件系统路由：app/page.tsx → /、app/about/page.tsx → /about
- 布局：`app/layout.tsx` 根布局，嵌套布局自动嵌套
- 加载状态：`app/loading.tsx` 自动loading UI
- 错误处理：`app/error.tsx` 错误边界
- 404页面：`app/not-found.tsx`
- 路由分组：`(group)/` 括号创建逻辑分组，不影响URL
- 平行路由：`@modal` 命名插槽，同一路由同时渲染多个页面
- 拦截路由：`(.)` 同级、`(..)` 上级、`(..)(..)` 根级拦截

## 渲染策略
- SSR（服务端渲染）：每次请求在服务端生成HTML，动态内容
- SSG（静态生成）：构建时生成HTML，适合内容不常变化的页面
- ISR（增量静态再生）：静态页面可在指定时间后重新生成
- RSC（React Server Components）：默认在服务端渲染，减少客户端JS
- "use client"：标记客户端组件，可使用useState、useEffect等
- Server Actions："use server" 标记的服务端函数，表单直接调用
- 默认所有组件都是Server Component，只有需要交互时才标记"use client"

## 数据获取
- Server Component中直接fetch：`const data = await fetch('https://api.example.com/data')`
- 无需useEffect：服务端组件直接async/await获取数据
- 缓存策略：`fetch(url, { cache: 'no-store' })` 不缓存、`{ next: { revalidate: 60 } }` 60秒重新验证
- 路由处理器：`app/api/users/route.ts` 定义API端点
  ```ts
  export async function GET() { return Response.json(users) }
  export async function POST(request: Request) { const data = await request.json(); }
  ```
- Server Actions：表单提交直接调用服务端函数，无需API层
- 数据库：Prisma、Drizzle等ORM直接在Server Component中使用

## 部署与优化
- 图片优化：`<Image src="/photo.jpg" width={500} height={300} />` 自动优化
- 字体优化：`next/font` 自动内联字体，避免布局偏移
- 元数据：`export const metadata = { title: 'My App' }` SEO优化
- 中间件：`middleware.ts` 请求前处理，如重定向、认证检查
- 部署方式：Vercel（推荐一键部署）、Docker、Node.js服务器
- 性能优化：自动代码分割、Tree Shaking、图片懒加载
- 环境变量：`.env.local` 本地开发、`NEXT_PUBLIC_` 前缀暴露到客户端
