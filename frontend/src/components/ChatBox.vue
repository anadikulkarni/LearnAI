<template>
  <div class="llm-chatbox-container">
    <div class="llm-container">
      <h1 class="chatbot-heading">AI Chat Bot</h1>
      <div class="llm-messageBox">
        <template v-for="(message, index) in messages" :key="index">
          <div :class="message.from === 'user' ? 'llm-messageCard llm-userCard' : 'llm-messageCard llm-chatGptCard'">
            <div :class="message.from === 'user' ? 'llm-cardContent llm-userCardContent' : 'llm-cardContent llm-chatGptCardContent'">
              <p v-html="formatMessage(message.data)"></p>
            </div>
          </div>
        </template>
        <!-- Spinner -->
        <div v-if="spinnerState" class="loading-spinner"></div>
      </div>
      <div class="llm-inputContainer">
        <input
          v-model="currentMessage"
          type="text"
          class="llm-messageInput"
          placeholder="Ask me anything..."
        />
        <button
          @click="sendMessage(currentMessage)"
          class="llm-askButton"
        >
          Ask
        </button>
        <button
          @click="clearMessages"
          class="llm-clearButton"
        >
          Clear
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { EventBus } from '../utils/eventBus.js'; // Import EventBus
import { marked } from 'marked';

export default {
  name: 'ChatBox',
  data() {
    return {
      currentMessage: '',
      messages: [],
      spinnerState: JSON.parse(localStorage.getItem('spinnerState')) || false, // Initialize from localStorage
    };
  },
  created() {
    EventBus.$on('new-message', (message) => {
      this.messages.push(message);
    });
    EventBus.$on('user-message', (message) => {
      this.messages.push(message);
    });
    EventBus.$on('show-spinner', () => {
      this.showSpinner();
    });
    EventBus.$on('hide-spinner', () => {
      this.hideSpinner();
    });
  },
  methods: {
    showSpinner() {
      this.spinnerState = true;
      localStorage.setItem('spinnerState', JSON.stringify(this.spinnerState));
    },
    hideSpinner() {
      this.spinnerState = false;
      localStorage.setItem('spinnerState', JSON.stringify(this.spinnerState));
    },
    async sendMessage(message) {
      if (!message) return; // Prevent sending empty messages

      this.messages.push({ from: 'user', data: message });
      this.currentMessage = ''; // Clear the input box after sending the message
      this.showSpinner(); // Show loading spinner

      try {
        const response = await axios.post('http://127.0.0.1:5000/api/llm/chatbot', { query: message });
        this.messages.push({ from: 'chatGpt', data: response.data.answer });
      } catch (error) {
        console.error('Error sending message:', error);
      } finally {
        this.hideSpinner(); // Hide loading spinner
      }
    },
    clearMessages() {
      this.messages = [];
      this.messages.push({ from: 'chatGpt', data: "hello, I'm your AI Learning assistant, Quick note: If no lecture, quiz or code is selected, I'll generate a random sample for you :)"});
    },
    formatMessage(message) {
      return marked(message); // Convert Markdown to HTML
    }
  },
};
</script>

<style>
.loading-spinner {
  border: 8px solid #f3f3f3;
  border-top: 8px solid #1877F2;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 20px auto; /* Center the spinner horizontally */
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.chatbot-heading {
  font-size: 18px;
  font-weight: 500;
  text-align: center;
  color: #222;
  padding: 8px;
  margin: 0;
  background-color: #f7f7f7;
  border-bottom: 1px solid #e7e7e7;
}

.llm-chatbox-container {
  position: relative;
  width: 770px; /* Fixed width */
  height: 800px; /* Fixed height */
  max-height: 100%; /* Prevent overflow beyond sidebar */
  overflow: hidden; /* Hide overflow within the container */
}

.llm-container {
  height: 100%; /* Fill the container's height */
  width: 100%; /* Fill the container's width */
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden; /* Hide overflow within the container */
  font-family: 'Roboto', sans-serif;
}

.llm-messageBox {
  flex-grow: 1;
  overflow-y: auto; /* Enable vertical scrolling */
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 8px;
}

.llm-inputContainer {
  display: flex;
  align-items: center;
  padding: 8px;
  background-color: #f0f0f0;
}

.llm-messageInput {
  flex-grow: 1;
  border: none;
  outline: none;
  padding: 8px;
  font-size: 14px;
  background-color: white;
  border-radius: 24px;
  margin-right: 8px;
}

.llm-cardContent {
  max-width: calc(100% - 10px); /* Adjusting for left and right margin */
  margin: 0 5px; /* 5px margin from left and right */
  padding: 8px;
  border-radius: 8px;
  font-size: 12px;
  line-height: 1.5;
}

.llm-userCardContent {
  background-color: #1877F2;
  color: white;
}

.llm-chatGptCardContent {
  background-color: #EDEDED;
  color: #222;
}

.llm-askButton {
  background-color: #1877F2;
  color: white;
  font-size: 14px;
  padding: 8px 12px;
  border: none;
  outline: none;
  cursor: pointer;
  border-radius: 24px;
  transition: background-color 0.3s ease-in-out;
}

.llm-askButton:hover {
  background-color: #145CB3;
}

.llm-clearButton {
  background-color: #FF4C4C;
  color: white;
  font-size: 14px;
  padding: 8px 12px;
  border: none;
  outline: none;
  cursor: pointer;
  border-radius: 24px;
  transition: background-color 0.3s ease-in-out;
  margin-left: 8px;
}

.llm-clearButton:hover {
  background-color: #E03A3A;
}
</style>
