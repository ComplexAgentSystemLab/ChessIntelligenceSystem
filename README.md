# ChessIntelligenceSystem

## 项目简介

`ChessIntelligenceSystem` 致力于为多种棋类（如国际象棋、中国象棋、围棋等）提供基于 PyTorch 的 AI 推理与训练服务。主要功能包括：

- 棋局状态解析与合法走子生成
- AI 模型推理（神经网络、搜索算法、符号主义AI、强化学习、仿生算法等）
- 支持模型训练、评估与管理
- 对外提供标准化 HTTP API，便于前端或其他系统调用

## API 对接规范

### 主要接口

- `POST /v1/chess/think`  
  接收棋局状态 JSON，返回推荐走法、置信度、评估值等。

#### 请求示例

```json
{
  "game": "chess",
  "model": "optional-model-name",
  "payload": {
    "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "legalMovesUci": null
  }
}
```

#### 成功响应示例

```json
{
  "ok": true,
  "payload": {
    "best": { "move": "e2e4", "confidence": 0.23, "value": 0.12 }
  }
}
```

#### 失败响应示例

```json
{
  "ok": false,
  "error": { "message": "模型未加载" }
}
```

### 说明

- 通过 `game` 字段区分不同棋类，便于扩展。
- 推荐本地开发监听 `http://127.0.0.1:8000`，保证接口稳定、响应及时。
- 详细协议可参考前端项目 `src/ai/README.md`。

## 部署与开发

1. 克隆本项目并安装依赖
2. 启动服务，确保接口可用
3. 按照接口协议与前端 `chess-games-react` 联调

## 与 chess-games-react 联调（最小可运行）

当前阶段为了尽量减少依赖，不引入任何棋类规则工具包（如 python-chess）。
因此服务端 **不会解析 FEN，也不会自行生成合法走法**，仅用于验证对接环境是否可用：

- 前端传入 `payload.legalMovesUci`（合法走法列表，UCI 字符串）
- 后端在该列表里做 **随机选择**，返回 `best`/`candidates`

> 换句话说：这是“对接烟测模式”，后续你接入真正 AI/规则引擎时，再把随机策略替换掉即可。

### 启动服务（开发）

在本项目根目录：

```powershell
uv pip install -e .
uv pip install -e ".[dev]"
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

启动后：
- 健康检查：`GET http://127.0.0.1:8000/health`
- 推理接口：`POST http://127.0.0.1:8000/v1/chess/think`

### 前端配置

前端默认会请求 `http://127.0.0.1:8000`（见 `chess-games-react/src/ai/orchestrator/useChessAiOrchestrator.ts`）。
确保后端运行在该地址即可直接联调。

### 运行测试

```powershell
python -m pytest
```

## 维护与文档

- 提供详细接口文档和示例代码，便于前端和其他调用方理解和接入。
- 支持多种 AI 应用场景，持续扩展棋类和模型能力。
