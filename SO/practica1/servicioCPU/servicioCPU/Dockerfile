FROM mcr.microsoft.com/dotnet/runtime:6.0 AS base
WORKDIR /app

FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
ARG BUILD_CONFIGURATION=Release
WORKDIR /src
COPY ["servicioCPU/servicioCPU.csproj", "servicioCPU/"]
RUN dotnet restore "servicioCPU/servicioCPU.csproj"
COPY . .
WORKDIR "/src/servicioCPU"
RUN dotnet build "servicioCPU.csproj" -c $BUILD_CONFIGURATION -o /app/build

FROM build AS publish
ARG BUILD_CONFIGURATION=Release
RUN dotnet publish "servicioCPU.csproj" -c $BUILD_CONFIGURATION -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "servicioCPU.dll"]
