# Next.js框架

## 核心知识点

### 一、App Router

```tsx
// app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
        <html lang="zh">
            <body>
                <nav>
                    <Link href="/">Home</Link>
                    <Link href="/about">About</Link>
                </nav>
                {children}
            </body>
        </html>
    );
}

// app/page.tsx
export default function HomePage() {
    return <h1>Welcome to Next.js</h1>;
}

// app/about/page.tsx
export default function AboutPage() {
    return <h1>About Us</h1>;
}

// app/users/[id]/page.tsx
export default async function UserPage({ params }: { params: { id: string } }) {
    const user = await fetchUser(params.id);
    return <div>{user.name}</div>;
}
```

### 二、Server Components

```tsx
// 默认是Server Component
async function UserList() {
    const users = await db.query('SELECT * FROM users');

    return (
        <ul>
            {users.map(user => (
                <li key={user.id}>{user.name}</li>
            ))}
        </ul>
    );
}

// Client Component
'use client';
import { useState } from 'react';

function Counter() {
    const [count, setCount] = useState(0);
    return (
        <div>
            <p>{count}</p>
            <button onClick={() => setCount(c => c + 1)}>+</button>
        </div>
    );
}
```

### 三、数据获取

```tsx
// Server Component中直接获取
async function PostsPage() {
    const posts = await fetch('https://api.example.com/posts', {
        cache: 'no-store' // 或 'force-cache'
    }).then(res => res.json());

    return <PostList posts={posts} />;
}

// Route Handlers (API Routes)
// app/api/users/route.ts
import { NextResponse } from 'next/server';

export async function GET() {
    const users = await db.query('SELECT * FROM users');
    return NextResponse.json(users);
}

export async function POST(request: Request) {
    const body = await request.json();
    const user = await db.insert(body);
    return NextResponse.json(user, { status: 201 });
}
```

### 四、Server Actions

```tsx
// app/actions.ts
'use server';

export async function createUser(formData: FormData) {
    const name = formData.get('name') as string;
    const email = formData.get('email') as string;

    await db.insert('users', { name, email });
    revalidatePath('/users');
}

// app/users/new/page.tsx
import { createUser } from '../actions';

export default function NewUserPage() {
    return (
        <form action={createUser}>
            <input name="name" placeholder="Name" required />
            <input name="email" type="email" placeholder="Email" required />
            <button type="submit">Create User</button>
        </form>
    );
}
```

### 五、静态生成与增量生成

```tsx
// 静态生成
export async function generateStaticParams() {
    const posts = await fetch('https://api.example.com/posts').then(r => r.json());
    return posts.map(post => ({ id: post.id.toString() }));
}

// 动态元数据
export async function generateMetadata({ params }) {
    const post = await fetchPost(params.id);
    return {
        title: post.title,
        description: post.excerpt,
    };
}

// 增量静态再生成
export const revalidate = 60; // 每60秒重新生成

// app/posts/[id]/page.tsx
export default async function PostPage({ params }) {
    const post = await fetchPost(params.id);
    return (
        <article>
            <h1>{post.title}</h1>
            <div dangerouslySetInnerHTML={{ __html: post.content }} />
        </article>
    );
}
```

### 六、部署

```bash
# Vercel部署
npx vercel

# Docker部署
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```
