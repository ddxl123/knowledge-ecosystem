# SwiftUI

## SwiftUI基础概念
- SwiftUI：Apple的声明式UI框架，用Swift代码描述界面
- 核心思想：界面是状态的函数 `View = f(State)`
- 自动更新：状态变化时SwiftUI自动重新计算并更新界面
- 平台支持：iOS、macOS、watchOS、tvOS统一框架
- 预览（Preview）：Xcode实时预览，无需运行即可看到界面效果
- 要求：iOS 13+、Xcode 11+

## 视图与修饰符
- 视图协议：`struct MyView: View { var body: some View { ... } }`
- 基础视图：Text、Image、Button、TextField、Toggle、Slider、Picker
- 布局容器：VStack（垂直）、HStack（水平）、ZStack（层叠）、Grid（网格）
- Spacer：弹性空间，将视图推到一侧
- 修饰符（Modifier）：`.font(.title)`、`.padding()`、`.foregroundColor(.blue)`
- 修饰符顺序重要：先padding再background vs 先background再padding效果不同
- 视图组合：将复杂视图拆分为小组件

## 状态管理
- @State：视图内部的可变状态，`@State private var count = 0`
- @Binding：子视图绑定父视图的状态，`@Binding var count: Int`
- @ObservableObject：引用类型的状态对象（class），遵循ObservableObject协议
- @Published：ObservableObject中自动触发视图更新的属性
- @ObservedObject：在视图中观察ObservableObject
- @StateObject：视图拥有并创建ObservableObject实例（生命周期与视图绑定）
- @EnvironmentObject：从环境中注入的共享状态对象
- @Environment：读取系统环境值（colorScheme、locale等）

## 列表与导航
- List：高性能列表视图，`List(items) { item in Text(item.name) }`
- ForEach：动态生成视图，支持Identifiable或id参数
- NavigationStack（iOS 16+）：声明式导航，`NavigationLink("Detail", value: item)`
- navigationDestination：定义导航目标，`navigationDestination(for: Item.self) { ... }`
- Sheet：模态弹出，`.sheet(isPresented: $showSheet) { SheetView() }`
- Alert/ConfirmationDialog：`.alert("Title", isPresented: $showAlert) { ... }`
- 搜索：`.searchable(text: $searchText)` 搜索栏

## 动画与手势
- 隐式动画：`.animation(.easeInOut, value: count)` 值变化时自动动画
- 显式动画：`withAnimation(.spring()) { count += 1 }`
- 动画类型：.linear、.easeIn、.easeOut、.easeInOut、.spring()、.interactiveSpring()
- 过渡效果：.transition(.slide)、.transition(.opacity)、.transition(.scale)
- withTransition：`withAnimation { show.toggle() }` 配合if/else视图切换
- 手势：TapGesture、LongPressGesture、DragGesture、MagnificationGesture、RotationGesture
- 手势组合：.simultaneously（同时）、.sequenced（顺序）、.exclusively（互斥）
- matchedGeometryEffect：视图间共享几何属性，实现hero动画
