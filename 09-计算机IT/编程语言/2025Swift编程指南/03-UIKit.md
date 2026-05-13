# UIKit开发

## 核心知识点

### 一、视图控制器

#### 1. 基本视图控制器
```swift
class ViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .white
        setupUI()
    }

    private func setupUI() {
        let label = UILabel()
        label.text = "Hello, UIKit!"
        label.textAlignment = .center
        label.frame = CGRect(x: 0, y: 100, width: view.bounds.width, height: 50)
        view.addSubview(label)
    }
}
```

#### 2. 生命周期
```swift
class MyViewController: UIViewController {
    override func loadView() {
        super.loadView()
        // 创建视图层次结构
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        // 视图已加载，初始化UI
    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        // 视图即将显示
    }

    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        // 视图已显示
    }

    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        // 视图即将消失
    }
}
```

### 二、Auto Layout

```swift
let redView = UIView()
redView.backgroundColor = .red
redView.translatesAutoresizingMaskIntoConstraints = false
view.addSubview(redView)

NSLayoutConstraint.activate([
    redView.centerXAnchor.constraint(equalTo: view.centerXAnchor),
    redView.centerYAnchor.constraint(equalTo: view.centerYAnchor),
    redView.widthAnchor.constraint(equalToConstant: 200),
    redView.heightAnchor.constraint(equalToConstant: 200),
])
```

### 三、表格视图

```swift
class UserListViewController: UIViewController, UITableViewDataSource, UITableViewDelegate {
    let tableView = UITableView()
    let users = ["Alice", "Bob", "Charlie"]

    override func viewDidLoad() {
        super.viewDidLoad()
        tableView.dataSource = self
        tableView.delegate = self
        tableView.register(UITableViewCell.self, forCellReuseIdentifier: "cell")
        view.addSubview(tableView)
        tableView.frame = view.bounds
    }

    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return users.count
    }

    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "cell", for: indexPath)
        cell.textLabel?.text = users[indexPath.row]
        return cell
    }

    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        print("Selected: \(users[indexPath.row])")
    }
}
```

### 四、导航

```swift
// AppDelegate或SceneDelegate中
let navController = UINavigationController(rootViewController: UserListViewController())
window?.rootViewController = navController

// 推送新页面
let detailVC = UserDetailViewController()
navigationController?.pushViewController(detailVC, animated: true)

// 模态呈现
let modalVC = ModalViewController()
present(modalVC, animated: true)
```

### 五、故事板与Segue

```swift
// 通过Segue导航
override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
    if segue.identifier == "showDetail" {
        if let detailVC = segue.destination as? UserDetailViewController,
           let indexPath = tableView.indexPathForSelectedRow {
            detailVC.user = users[indexPath.row]
        }
    }
}

// 代码触发Segue
performSegue(withIdentifier: "showDetail", sender: self)
```
