# 🎯 下拉菜单式 Agent 切换功能

## 🆕 新界面特性

### 📋 主要改进
1. **下拉菜单选择器** - 位于页面顶部，方便快速切换
2. **实时状态显示** - 显示当前 Agent 状态和消息数量
3. **一键状态刷新** - 点击 🔄 按钮即可检查 Agent 状态
4. **智能配置管理** - 自动处理 Agent 配置和会话管理

### 🎨 界面布局

```
🤖 Bedrock Agent Chat Interface
Select an agent and start chatting - switches take effect immediately

[🤖 Select Bedrock Agent: ▼]  [Status: ✅ Available]  [Messages: 5]
                                      [🔄]

ℹ️ OCR Demo Agent for text extraction

[Custom Agent ID input - only shown for Custom Agent]

💬 Chat Area
├── User messages
└── Agent responses

💡 Tips: Use the dropdown above to switch agents instantly
```

### 🔄 Agent 切换流程

1. **选择 Agent**
   ```
   点击下拉菜单 → 选择目标 Agent → 立即生效
   ```

2. **状态检查**
   ```
   自动显示状态 → 点击🔄刷新 → 实时更新状态
   ```

3. **会话管理**
   ```
   切换Agent → 自动创建新会话 → 保持聊天历史
   ```

## 🎯 用户体验优化

### ✅ 优点
- **直观操作**: 下拉菜单比单选按钮更直观
- **节省空间**: 主界面更简洁，侧边栏专注于会话管理
- **快速切换**: 一次点击即可切换 Agent
- **状态可见**: 实时显示 Agent 状态和消息统计

### 🚀 实时生效
- 无需重启应用
- 切换后立即可用
- 自动会话管理
- 配置状态同步

## 📱 界面组件说明

### 1. Agent 选择器
```
🤖 Select Bedrock Agent: [Agent 2 - OCR Demo ▼]
```
- 显示当前选中的 Agent
- 点击展开所有可用 Agent
- 选择后立即切换

### 2. 状态指示器
```
Status: ✅ Available  [🔄]
```
- ✅ Available: Agent 可用
- ❌ Agent Not Found: Agent 不存在
- 🔒 Access Denied: 权限不足
- 🔄 按钮: 手动刷新状态

### 3. 消息统计
```
Messages: 5
```
- 显示当前会话的消息数量
- 实时更新

### 4. 自定义 Agent 输入
```
Enter your Agent ID: [ABCDEF1234        ]
Current Config: ID: ABCDEF1234
               Region: us-west-2
```
- 仅在选择 "Custom Agent" 时显示
- 支持实时输入和验证

## 🔧 技术实现

### 状态管理
```python
# 实时状态更新
if selected_agent != st.session_state.selected_agent:
    st.session_state.selected_agent = selected_agent
    update_agent_configuration(selected_agent)
    st.success(f"✅ Switched to {selected_agent}")
    st.rerun()
```

### 配置同步
```python
# 自动配置更新
def update_agent_configuration(selected_agent, custom_id=None):
    # 更新 Agent 配置
    # 重置会话 ID
    # 清除状态缓存
```

### 界面响应
```python
# 三列布局
col1, col2, col3 = st.columns([3, 1, 1])
with col1: # Agent 选择器
with col2: # 状态显示
with col3: # 消息统计
```

## 🎉 使用方法

### 快速开始
```bash
cd streamlint-client
./run_app.sh
```

### 手动启动
```bash
streamlit run app.py
```

### 测试配置
```bash
python test_config.py
```

## 💡 使用技巧

1. **快速切换**: 使用下拉菜单在不同 Agent 间快速切换
2. **状态监控**: 定期点击🔄按钮检查 Agent 状态
3. **自定义测试**: 使用 Custom Agent 选项测试新的 Agent ID
4. **会话管理**: 利用侧边栏的清除和新建会话功能
5. **配置查看**: 在侧边栏查看详细的配置信息

## 🔍 故障排除

### 常见问题
1. **Agent 不可用**: 检查 Agent ID 是否正确
2. **权限错误**: 验证 AWS 凭证和权限
3. **网络问题**: 确认网络连接和 AWS 服务状态

### 调试步骤
1. 点击🔄按钮检查 Agent 状态
2. 查看侧边栏的配置信息
3. 运行 `python test_config.py` 进行诊断
