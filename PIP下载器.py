import os
import sys
import urllib.request
import subprocess

def download_package(package_name, mirror="https://pypi.tuna.tsinghua.edu.cn/simple", options={}):
    """
    从指定镜像源下载Python包
    参数说明:
    - package_name: 包名
    - mirror: pip镜像源
    - upgrade: 是否升级到最新版本
    - force: 是否强制重新安装
    - user: 是否安装到用户目录
    - no_deps: 是否不安装依赖
    - no_cache: 是否不使用缓存
    """
    try:
        # 构建pip命令参数
        pip_args = [sys.executable, "-m", "pip", "install", f"--index-url={mirror}"]
        
        for option, value in options.items():
            if value:
                pip_args.append(option)
                if isinstance(value, list):
                    pip_args.append(" ".join(str(x) for x in value))
                elif isinstance(value, bool):
                    pip_args.append(value)
                else:
                    pip_args.append(str(value))
                
        pip_args.append(package_name)
        
        # 尝试使用pip安装
        print(f"正在尝试使用pip安装 {package_name}...")
        result = subprocess.run(pip_args, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"{package_name} 安装成功!")
            return True
        else:
            # 检查是否为pip命令未找到的错误
            if result.stderr.startswith("pip :"):
                # pip命令未找到,添加系统环境变量
                print("pip命令未找到,正在添加系统环境变量...")
                python_path = subprocess.check_output(["python", "-c", "import sys; print(sys.executable)"], text=True).strip()
                scripts_path = os.path.join(os.path.dirname(python_path), "Scripts")
                
                # 获取当前环境变量
                path = os.environ.get("PATH", "")
                
                if python_path not in path:
                    os.environ["PATH"] = f"{python_path};{path}"
                if scripts_path not in path:    
                    os.environ["PATH"] = f"{scripts_path};{path}"
                    
                # 重新尝试安装
                print("正在重新尝试安装...")
                result = subprocess.run(pip_args, capture_output=True, text=True)
                                       
                if result.returncode == 0:
                    print(f"{package_name} 安装成功!")
                    return True
                else:
                    print(f"安装失败: {result.stderr}")
                    return False
            else:
                print(f"安装失败: {result.stderr}")
                return False
            
    except Exception as e:
        print(f"安装出错: {str(e)}")
        return False

def list_packages():
    """列出已安装的包"""
    result = subprocess.run([sys.executable, "-m", "pip", "list"], capture_output=True, text=True)
    print(result.stdout)

def uninstall_package(package_name, yes=False):
    """卸载指定的包"""
    pip_args = [sys.executable, "-m", "pip", "uninstall"]
    if yes:
        pip_args.append("-y")
    pip_args.append(package_name)
    
    result = subprocess.run(pip_args, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"{package_name} 卸载成功!")
        return True
    else:
        print(f"卸载失败: {result.stderr}")
        return False

def show_package_info(package_name):
    """显示包的详细信息"""
    result = subprocess.run([sys.executable, "-m", "pip", "show", package_name], capture_output=True, text=True)
    print(result.stdout)

def main():
    print("""命令:
    install                     安装包
    download                    下载包
    uninstall                   卸载包
    freeze                      以requirements格式输出已安装的包
    inspect                     检查Python环境
    list                       列出已安装的包
    show                       显示已安装包的信息
    check                      验证已安装包的依赖兼容性
    config                     管理本地和全局配置
    search                     在PyPI中搜索包
    cache                      检查和管理pip的wheel缓存
    index                      检查包索引中的可用信息
    wheel                      从requirements构建wheels
    hash                       计算包存档的哈希值
    completion                 用于命令补全的帮助命令
    debug                      显示调试有用的信息
    help                       显示帮助信息

常用选项:
    -h, --help                 显示帮助
    --debug                    让未处理的异常传播到主程序外
    --isolated                 在隔离模式下运行pip
    --require-virtualenv       仅允许在虚拟环境中运行pip
    --python <python>          使用指定的Python解释器运行pip
    -v, --verbose             输出更多信息
    -V, --version             显示版本并退出
    -q, --quiet               减少输出信息
    --no-cache-dir            禁用缓存
    --user                    安装到用户目录
    --no-deps                 不安装依赖
    --force                   强制重新安装
    --upgrade                 升级到最新版本
    """)

    command = input("请输入命令: ")
    
    if command in ["install", "download"]:
        package_name = input("请输入包名: ")
        
        params = {}
        
        print("\n可选参数(True/False):")
        params_ = input("请输入参数表: ")
        if params_ == "":
            params = {}
        else:
            params = eval(params_)

        download_package(package_name,
                        options=params)
                        
    elif command == "uninstall":
        package_name = input("请输入要卸载的包名: ")
        yes = input("是否确认卸载? (y/n): ").lower() == 'y'
        uninstall_package(package_name, yes)
        
    elif command in ["list", "freeze"]:
        list_packages()
        
    elif command in ["show", "inspect"]:
        package_name = input("请输入包名: ")
        show_package_info(package_name)
        
    elif command == "help":
        main()
        
    else:
        print("无效的命令!")

if __name__ == "__main__":
    main()
