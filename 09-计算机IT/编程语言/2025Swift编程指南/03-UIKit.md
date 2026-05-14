# UIKit

## UIKit基础架构
- UIKit：iOS传统的UI框架，基于命令式编程和MVC模式
- UIResponder：所有可响应事件的对象的基类
- UIWindow：应用的窗口，通常只有一个主窗口
- UIView：所有可视化组件的基类，管理屏幕上的一块矩形区域
- UIViewController：管理一组视图，处理用户交互和生命周期
- MVC模式：Model（数据）、View（界面）、Controller（协调）

## 视图与布局
- 视图层级：addSubview()添加、removeFromSuperview()移除
- Frame布局：直接设置view.frame = CGRect(x, y, width, height)
- Auto Layout：约束式布局，定义视图间的关系而非固定位置
- NSLayoutConstraint：`view.widthAnchor.constraint(equalToConstant: 100)`
- 常用约束：widthAnchor、heightAnchor、leadingAnchor、trailingAnchor、topAnchor、bottomAnchor
- UIStackView：自动布局的容器，水平或垂直排列子视图
- Safe Area：避开刘海和Home指示器的安全区域

## 常用UI组件
- UILabel：显示文本，支持富文本、多行、自动调整大小
- UIButton：按钮，支持多种样式和状态
- UITextField：单行文本输入，支持占位符、键盘类型
- UITextView：多行文本编辑
- UIImageView：显示图片，支持Content Mode（scaleToFill、scaleAspectFit等）
- UITableView：列表视图，基于cell复用的高性能滚动
- UICollectionView：网格/自定义布局的集合视图
- UIScrollView：可滚动容器，支持缩放和分页

## 视图控制器生命周期
- loadView：创建视图层次结构（不常用，通常用Storyboard或XIB）
- viewDidLoad：视图加载完成，做初始化设置
- viewWillAppear：视图即将显示，刷新数据
- viewDidAppear：视图已显示，开始动画或网络请求
- viewWillDisappear：视图即将消失，保存状态
- viewDidDisappear：视图已消失
- viewWillLayoutSubviews：即将布局子视图
- viewDidLayoutSubviews：布局完成

## 导航与转场
- UINavigationController：导航栈，push/pop管理页面
- push与pop：`navigationController?.pushViewController(vc, animated: true)`
- UITabBarController：标签页控制器，底部标签切换
- Modal呈现：`present(vc, animated: true)` 模态弹出
- Segue：Storyboard中的页面跳转连线，prepare(for:sender:)传递数据
- 自定义转场动画：UIViewControllerAnimatedTransitioning协议
- 协议传值：delegate模式回传数据
- 闭包传值：通过闭包回调传递数据
