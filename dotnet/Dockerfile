# Dockerfile

# 使用镜像: microsoft aspnetcore 3.1
FROM mcr.microsoft.com/dotnet/core/aspnet:3.1

# 将publish下的内容复制到docker容器的/NjnuClassroom/dotnet目录下
COPY ./publish /NjnuClassroom/dotnet

# 设置工作目录为/NjnuClassroom/dotnet
WORKDIR /NjnuClassroom/dotnet

# 启动命令
ENTRYPOINT ["dotnet", "NjnuClassroom.dll"]
