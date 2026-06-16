# 用 NSSM 把两个进程注册为 Windows 服务 (自启 + 自动重启)
# 用法: 先安装 nssm 并把 nssm.exe 放入 PATH, 再以管理员运行本脚本
param(
  [string]$PyExe = "python",
  [string]$WorkDir = "C:\rope"
)
nssm install RopeEdge $PyExe "edge_main.py --config configs\edge.yaml"
nssm set RopeEdge AppDirectory $WorkDir
nssm set RopeEdge AppExit Default Restart
nssm install RopeForward $PyExe "forward.py --config configs\edge.yaml"
nssm set RopeForward AppDirectory $WorkDir
nssm set RopeForward AppExit Default Restart
Write-Host "已注册 RopeEdge / RopeForward 服务, 用 'nssm start RopeEdge' 启动"
