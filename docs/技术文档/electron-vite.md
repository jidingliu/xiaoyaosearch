https://cn.electron-vite.org/guide/

# 搭建第一个 electron-vite 项目
```
npm create @quick-start/electron@latest

```
然后按照提示操作即可!

你还可以通过附加的命令行选项直接指定项目名称和你想要使用的模板。例如，要构建一个 Electron + Vue 项目，运行:

```
# npm 7+，需要添加额外的 --：
npm create @quick-start/electron@latest my-app -- --template vue
```

# 克隆模板
create-electron 是一个快速生成主流 Electron 框架基础模板的工具。你还可以用如 degit 之类的工具，使用 electron-vite-boilerplate 模板来搭建项目。

```
npx degit alex8088/electron-vite-boilerplate electron-app
cd electron-app

npm install
npm run dev

```