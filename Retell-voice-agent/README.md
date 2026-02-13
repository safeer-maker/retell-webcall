This foulder will be the updated code and integration of variaous ai tool with retail ai.

## MCP integration

MCP integration of retall.ai if in mcp-integration.ipynb file.

## 🚀 Retell AI MCP Server Integration

## ✅ Setup Complete!

The Retell AI MCP server has been configured in VS Code settings (`.vscode/settings.json`)

## 📋 How to Use with GitHub Copilot

### 1. **Reload VS Code** (Important!)
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type: `Developer: Reload Window`
   - Or restart VS Code

### 2. **Open GitHub Copilot Chat**
   - Click the chat icon in the sidebar, OR
   - Press `Ctrl+Alt+I` (or `Cmd+Alt+I` on Mac)

### 3. **Use Retell AI Tools**
   You can now ask Copilot to use Retell AI tools directly:
   
   ```
   @workspace List all my Retell AI voice agents
   
   @workspace Get details for agent ID agent_594b1eb4983ebeb449c2e17c47
   
   @workspace Create a web call for my Appointment Booking Agent
   
   @workspace List all available voices in Retell AI
   
   @workspace Show me my recent phone calls
   ```

### 4. **Available Retell AI Tools via MCP**
   The MCP server provides access to all Retell AI capabilities:
   - 🤖 Agent Management (list, create, update, delete)
   - 📞 Phone & Web Calls 
   - 🔢 Phone Numbers
   - 🎙️ Voice Configuration
   - 🧠 LLM Settings
   - 📊 Analytics & Recordings

### 5. **Check MCP Server Status**
   In Copilot Chat, type: `@workspace #mcp` to see connected MCP servers

## 🔑 Configuration Location
- **Settings File**: `.vscode/settings.json`
- **API Key**: Loaded from environment variable
- **Server**: `@abhaybabbar/retellai-mcp-server` (via npx)

## 💡 Tips
- Use `@workspace` to ensure Copilot has full context
- The MCP server auto-starts when you use Copilot
- All API calls use your RETELL_API_KEY from the settings
