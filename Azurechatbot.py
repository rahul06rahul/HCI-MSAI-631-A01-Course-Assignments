<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Azure OpenAI Chatbot</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .chatbot-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 800px;
            height: 700px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .chatbot-header {
            background: linear-gradient(135deg, #0078d4, #106ebe);
            color: white;
            padding: 20px;
            text-align: center;
            position: relative;
        }

        .chatbot-header h1 {
            font-size: 24px;
            margin-bottom: 5px;
        }

        .chatbot-header p {
            font-size: 14px;
            opacity: 0.9;
        }

        .status-indicator {
            position: absolute;
            top: 20px;
            right: 20px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .status-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #28a745;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }

        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .message {
            max-width: 80%;
            padding: 12px 16px;
            border-radius: 18px;
            word-wrap: break-word;
            animation: fadeIn 0.3s ease-in;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .user-message {
            background: linear-gradient(135deg, #007bff, #0056b3);
            color: white;
            align-self: flex-end;
            margin-left: auto;
        }

        .bot-message {
            background: #f8f9fa;
            color: #333;
            align-self: flex-start;
            border: 1px solid #e9ecef;
        }

        .error-message {
            background: #ffe6e6;
            color: #d63384;
            border: 1px solid #f5c6cb;
        }

        .system-message {
            background: #e3f2fd;
            color: #1976d2;
            border: 1px solid #bbdefb;
            font-style: italic;
        }

        .input-container {
            padding: 20px;
            background: #f8f9fa;
            border-top: 1px solid #e9ecef;
            display: flex;
            gap: 10px;
        }

        .input-field {
            flex: 1;
            padding: 12px 16px;
            border: 2px solid #e9ecef;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s ease;
        }

        .input-field:focus {
            border-color: #007bff;
        }

        .send-button {
            background: linear-gradient(135deg, #28a745, #20c997);
            color: white;
            border: none;
            border-radius: 50%;
            width: 48px;
            height: 48px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.2s ease;
        }

        .send-button:hover {
            transform: scale(1.05);
        }

        .send-button:disabled {
            background: #6c757d;
            cursor: not-allowed;
            transform: none;
        }

        .quick-actions {
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
            flex-wrap: wrap;
        }

        .quick-action-btn {
            background: #e3f2fd;
            color: #1976d2;
            border: 1px solid #bbdefb;
            border-radius: 20px;
            padding: 8px 16px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.2s ease;
        }

        .quick-action-btn:hover {
            background: #1976d2;
            color: white;
        }

        .typing-indicator {
            display: none;
            align-items: center;
            gap: 5px;
            color: #6c757d;
            font-style: italic;
        }

        .typing-dots {
            display: flex;
            gap: 3px;
        }

        .typing-dots span {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #6c757d;
            animation: typing 1.4s infinite;
        }

        .typing-dots span:nth-child(2) { animation-delay: 0.2s; }
        .typing-dots span:nth-child(3) { animation-delay: 0.4s; }

        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-10px); }
        }

        .config-panel {
            background: #f8f9fa;
            padding: 15px;
            border-bottom: 1px solid #e9ecef;
            margin: 0;
        }

        .config-toggle {
            background: #007bff;
            color: white;
            border: none;
            padding: 8px 12px;
            border-radius: 5px;
            cursor: pointer;
            margin-bottom: 10px;
        }

        .config-form {
            display: none;
        }

        .config-form.active {
            display: block;
        }

        .config-form input {
            width: 100%;
            padding: 8px;
            margin: 5px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }

        .config-form button {
            background: #28a745;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            width: 100%;
        }

        @media (max-width: 768px) {
            .chatbot-container {
                height: 100vh;
                border-radius: 0;
            }
        }
    </style>
</head>
<body>
    <div class="chatbot-container">
        <div class="config-panel">
            <button class="config-toggle" onclick="toggleConfig()">⚙️ Configure Azure OpenAI</button>
            <div class="config-form" id="configForm">
                <h4>Azure OpenAI Configuration</h4>
                <input type="text" id="azureEndpoint" placeholder="Azure OpenAI Endpoint" value="">
                <input type="password" id="azureKey" placeholder="Azure OpenAI API Key" value="">
                <input type="text" id="deploymentName" placeholder="Deployment Name" value="gpt-35-turbo">
                <button onclick="saveConfig()">Save Configuration</button>
            </div>
        </div>

        <div class="chatbot-header">
            <h1>🤖 Azure OpenAI Chatbot</h1>
            <p>Powered by Azure Cognitive Services</p>
            <div class="status-indicator">
                <div class="status-dot"></div>
                <span id="statusText">Ready</span>
            </div>
        </div>

        <div class="chat-messages" id="chatMessages">
            <div class="message bot-message system-message">
                👋 Welcome! I'm your Azure OpenAI-powered chatbot. I'm here to help you with various tasks and questions.
                <br><br>
                <strong>🚀 My Capabilities:</strong>
                <br>• Answer questions and provide information
                <br>• Help with writing and content creation
                <br>• Assist with problem-solving and analysis
                <br>• Provide coding help and explanations
                <br>• Engage in creative conversations
                <br>• Handle multiple languages
                <br>• Maintain context throughout our conversation
                <br><br>
                <strong>⚙️ Setup Required:</strong> Please configure your Azure OpenAI credentials using the settings panel in the top-left corner.
            </div>
        </div>

        <div class="input-container">
            <div class="quick-actions">
                <button class="quick-action-btn" onclick="sendQuickMessage('What are your capabilities?')">💡 Capabilities</button>
                <button class="quick-action-btn" onclick="sendQuickMessage('Tell me a joke')">😄 Tell Joke</button>
                <button class="quick-action-btn" onclick="sendQuickMessage('Help me with coding')">💻 Code Help</button>
                <button class="quick-action-btn" onclick="sendQuickMessage('Explain quantum computing')">🔬 Explain Topic</button>
            </div>
            <div style="display: flex; gap: 10px; width: 100%;">
                <input type="text" class="input-field" id="messageInput" placeholder="Type your message here..." onkeypress="handleKeyPress(event)">
                <button class="send-button" id="sendButton" onclick="sendMessage()">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="22" y1="2" x2="11" y2="13"></line>
                        <polygon points="22,2 15,22 11,13 2,9"></polygon>
                    </svg>
                </button>
            </div>
            <div class="typing-indicator" id="typingIndicator">
                <span>Bot is typing</span>
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Configuration variables
        let azureConfig = {
            endpoint: '',
            key: '',
            deploymentName: 'gpt-35-turbo'
        };

        // Chat state
        let conversationHistory = [];
        let isConfigured = false;

        // Initialize the application
        function init() {
            loadConfig();
            checkConfiguration();
            addMessage('system', '🔧 To get started, please configure your Azure OpenAI settings using the configuration panel.');
        }

        // Configuration functions
        function toggleConfig() {
            const configForm = document.getElementById('configForm');
            configForm.classList.toggle('active');
        }

        function saveConfig() {
            const endpoint = document.getElementById('azureEndpoint').value.trim();
            const key = document.getElementById('azureKey').value.trim();
            const deployment = document.getElementById('deploymentName').value.trim();

            if (!endpoint || !key || !deployment) {
                alert('Please fill in all configuration fields');
                return;
            }

            azureConfig = {
                endpoint: endpoint.endsWith('/') ? endpoint.slice(0, -1) : endpoint,
                key: key,
                deploymentName: deployment
            };

            // Store in memory (not localStorage as per restrictions)
            isConfigured = true;
            updateStatus('Configured', 'green');
            
            addMessage('system', '✅ Azure OpenAI configuration saved successfully! You can now start chatting.');
            document.getElementById('configForm').classList.remove('active');
        }

        function loadConfig() {
            // Pre-populate with your Azure details
            document.getElementById('azureEndpoint').value = 'https://openaichatbotrahul.openai.azure.com/';
            document.getElementById('deploymentName').value = 'gpt-35-turbo';
        }

        function checkConfiguration() {
            if (!isConfigured) {
                updateStatus('Not Configured', 'orange');
                return false;
            }
            updateStatus('Ready', 'green');
            return true;
        }

        function updateStatus(text, color) {
            const statusText = document.getElementById('statusText');
            const statusDot = document.querySelector('.status-dot');
            statusText.textContent = text;
            statusDot.style.background = color === 'green' ? '#28a745' : color === 'orange' ? '#ffc107' : '#dc3545';
        }

        // Message handling functions
        function addMessage(type, content, isError = false) {
            const messagesContainer = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            
            let className = 'message ';
            if (type === 'user') {
                className += 'user-message';
            } else if (type === 'system') {
                className += 'system-message';
            } else if (isError) {
                className += 'error-message';
            } else {
                className += 'bot-message';
            }
            
            messageDiv.className = className;
            messageDiv.innerHTML = content.replace(/\n/g, '<br>');
            
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        function showTypingIndicator() {
            document.getElementById('typingIndicator').style.display = 'flex';
        }

        function hideTypingIndicator() {
            document.getElementById('typingIndicator').style.display = 'none';
        }

        function sendQuickMessage(message) {
            document.getElementById('messageInput').value = message;
            sendMessage();
        }

        async function sendMessage() {
            const messageInput = document.getElementById('messageInput');
            const sendButton = document.getElementById('sendButton');
            const message = messageInput.value.trim();

            if (!message) {
                addMessage('system', '⚠️ Please enter a message before sending.', true);
                return;
            }

            if (!checkConfiguration()) {
                addMessage('system', '⚠️ Please configure your Azure OpenAI settings first.', true);
                return;
            }

            // Disable input and show user message
            sendButton.disabled = true;
            messageInput.value = '';
            addMessage('user', message);

            // Handle special commands
            if (message.toLowerCase().includes('capabilities') || message.toLowerCase().includes('what can you do')) {
                handleCapabilitiesRequest();
                sendButton.disabled = false;
                return;
            }

            // Validate and clean input
            const cleanedMessage = validateAndCleanInput(message);
            if (!cleanedMessage) {
                addMessage('bot', "I'm sorry, but I couldn't process that input. Please try rephrasing your question or request.", true);
                sendButton.disabled = false;
                return;
            }

            showTypingIndicator();

            try {
                const response = await callAzureOpenAI(cleanedMessage);
                hideTypingIndicator();
                addMessage('bot', response);
                
                // Add to conversation history
                conversationHistory.push({user: cleanedMessage, bot: response});
                
            } catch (error) {
                hideTypingIndicator();
                console.error('Error calling Azure OpenAI:', error);
                handleAPIError(error);
            }

            sendButton.disabled = false;
        }

        function validateAndCleanInput(input) {
            // Handle malformed input
            if (!input || typeof input !== 'string') {
                return null;
            }

            // Remove excessive whitespace
            input = input.trim().replace(/\s+/g, ' ');

            // Check for minimum length
            if (input.length < 1) {
                return null;
            }

            // Check for maximum length (adjust as needed)
            if (input.length > 4000) {
                return input.substring(0, 4000) + '...';
            }

            // Handle common malformed patterns
            if (input.match(/^[!@#$%^&*()_+={}[\]|\\:";'<>?,./]*$/)) {
                return null; // Only special characters
            }

            return input;
        }

        function handleCapabilitiesRequest() {
            const capabilities = `
🚀 <strong>My Capabilities Include:</strong>

<strong>💬 Conversational AI:</strong>
• Natural language understanding and generation
• Context-aware responses
• Multi-turn conversations

<strong>📝 Content Creation:</strong>
• Writing assistance (emails, articles, stories)
• Text summarization and analysis
• Grammar and style suggestions

<strong>💻 Technical Support:</strong>
• Code explanation and debugging
• Programming help in multiple languages
• Technical documentation assistance

<strong>🧠 Problem Solving:</strong>
• Analytical thinking and reasoning
• Step-by-step problem breakdown
• Creative solution generation

<strong>🌍 Knowledge & Information:</strong>
• General knowledge questions
• Explanations of complex topics
• Research and fact-checking assistance

<strong>🎨 Creative Tasks:</strong>
• Creative writing and storytelling
• Brainstorming ideas
• Content ideation

<strong>🔧 Error Handling:</strong>
• Input validation and cleaning
• Graceful handling of malformed queries
• Context-aware error recovery

<strong>☁️ Cloud Integration:</strong>
• Powered by Azure OpenAI Services
• Scalable and reliable AI processing
• Enterprise-grade security and compliance

Feel free to ask me anything or try any of these capabilities!
            `;
            addMessage('bot', capabilities);
        }

        async function callAzureOpenAI(message) {
            const url = `${azureConfig.endpoint}/openai/deployments/${azureConfig.deploymentName}/chat/completions?api-version=2024-02-15-preview`;
            
            const systemPrompt = `You are a helpful AI assistant powered by Azure OpenAI. You should:
1. Provide accurate and helpful responses
2. Be conversational and friendly
3. Ask clarifying questions when needed
4. Handle errors gracefully
5. Provide detailed explanations when requested
6. Be concise but thorough
7. Acknowledge when you don't know something`;

            const messages = [
                {"role": "system", "content": systemPrompt}
            ];

            // Add conversation history (last 5 exchanges to manage token limits)
            const recentHistory = conversationHistory.slice(-5);
            for (const exchange of recentHistory) {
                messages.push({"role": "user", "content": exchange.user});
                messages.push({"role": "assistant", "content": exchange.bot});
            }

            messages.push({"role": "user", "content": message});

            const requestBody = {
                messages: messages,
                max_tokens: 1000,
                temperature: 0.7,
                top_p: 0.9,
                frequency_penalty: 0.1,
                presence_penalty: 0.1
            };

            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'api-key': azureConfig.key
                },
                body: JSON.stringify(requestBody)
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            
            if (data.choices && data.choices.length > 0) {
                return data.choices[0].message.content;
            } else {
                throw new Error('No response generated');
            }
        }

        function handleAPIError(error) {
            let errorMessage = "I'm sorry, I encountered an error while processing your request. ";
            
            if (error.message.includes('401')) {
                errorMessage += "Please check your API key configuration.";
            } else if (error.message.includes('404')) {
                errorMessage += "Please verify your endpoint URL and deployment name.";
            } else if (error.message.includes('429')) {
                errorMessage += "Rate limit exceeded. Please try again in a moment.";
            } else if (error.message.includes('500')) {
                errorMessage += "Azure OpenAI service is temporarily unavailable.";
            } else {
                errorMessage += "Please try again or check your configuration.";
            }
            
            errorMessage += "\n\n🔧 <strong>Troubleshooting Tips:</strong>";
            errorMessage += "\n• Verify your Azure OpenAI endpoint URL";
            errorMessage += "\n• Check that your API key is correct";
            errorMessage += "\n• Ensure your deployment name matches your Azure setup";
            errorMessage += "\n• Confirm your Azure subscription is active";
            
            addMessage('bot', errorMessage, true);
            updateStatus('Error', 'red');
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                sendMessage();
            }
        }

        // Initialize the application when the page loads
        window.onload = init;
    </script>
</body>
</html>
