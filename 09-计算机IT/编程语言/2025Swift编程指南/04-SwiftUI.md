# SwiftUI开发

## 核心知识点

### 一、基本视图

```swift
struct ContentView: View {
    var body: some View {
        VStack(spacing: 20) {
            Text("Hello, SwiftUI!")
                .font(.largeTitle)
                .foregroundColor(.blue)

            Image(systemName: "star.fill")
                .resizable()
                .frame(width: 50, height: 50)
                .foregroundColor(.yellow)

            Button("Tap Me") {
                print("Button tapped")
            }
            .buttonStyle(.borderedProminent)
        }
        .padding()
    }
}
```

### 二、列表与导航

```swift
struct UserListView: View {
    let users = ["Alice", "Bob", "Charlie"]

    var body: some View {
        NavigationStack {
            List(users, id: \.self) { user in
                NavigationLink(user) {
                    UserDetailView(name: user)
                }
            }
            .navigationTitle("Users")
        }
    }
}

struct UserDetailView: View {
    let name: String

    var body: some View {
        Text("Details for \(name)")
            .navigationTitle(name)
    }
}
```

### 三、状态管理

#### 1. @State
```swift
struct CounterView: View {
    @State private var count = 0

    var body: some View {
        VStack {
            Text("Count: \(count)")
            Button("Increment") {
                count += 1
            }
        }
    }
}
```

#### 2. @Binding
```swift
struct ToggleView: View {
    @Binding var isOn: Bool

    var body: some View {
        Toggle("Enable Feature", isOn: $isOn)
    }
}

struct ParentView: View {
    @State private var featureEnabled = false

    var body: some View {
        ToggleView(isOn: $featureEnabled)
    }
}
```

#### 3. @ObservableObject
```swift
class UserViewModel: ObservableObject {
    @Published var users: [String] = []
    @Published var isLoading = false

    func fetchUsers() {
        isLoading = true
        // 模拟网络请求
        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
            self.users = ["Alice", "Bob", "Charlie"]
            self.isLoading = false
        }
    }
}

struct UserListPage: View {
    @StateObject private var viewModel = UserViewModel()

    var body: some View {
        List(viewModel.users, id: \.self) { user in
            Text(user)
        }
        .overlay {
            if viewModel.isLoading {
                ProgressView()
            }
        }
        .onAppear {
            viewModel.fetchUsers()
        }
    }
}
```

### 四、动画

```swift
struct AnimatedView: View {
    @State private var isExpanded = false

    var body: some View {
        VStack {
            RoundedRectangle(cornerRadius: 10)
                .fill(Color.blue)
                .frame(width: isExpanded ? 300 : 100,
                       height: isExpanded ? 200 : 100)
                .animation(.spring(response: 0.5, dampingFraction: 0.6), value: isExpanded)

            Button("Toggle") {
                isExpanded.toggle()
            }
        }
    }
}
```

### 五、表单与用户输入

```swift
struct SettingsView: View {
    @State private var username = ""
    @State private var notificationsEnabled = true
    @State private var fontSize = 16.0

    var body: some View {
        Form {
            Section("Profile") {
                TextField("Username", text: $username)
            }

            Section("Preferences") {
                Toggle("Notifications", isOn: $notificationsEnabled)
                HStack {
                    Text("Font Size")
                    Slider(value: $fontSize, in: 10...30, step: 1)
                    Text("\(Int(fontSize))")
                }
            }

            Section {
                Button("Save") {
                    // 保存设置
                }
            }
        }
        .navigationTitle("Settings")
    }
}
```
