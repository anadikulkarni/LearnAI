<script setup>

import axios from 'axios';
import qs from 'qs';

const languageMapping = {
  python: 'py',
  java: 'java',
  cpp: 'cpp',
  c: 'c',
  go: 'go',
  csharp: 'cs',
  javascript: 'js'
};

const compileCode = async () => {
  try {
    // Retrieve code from localStorage or use default
    let code = localStorage.getItem('current_code') || `def example_function(x): return x * 2; print(example_function(5))`;
    let editorLanguage = localStorage.getItem('current_language') || 'python';
    let code_input = localStorage.getItem('code_input') || '';
    let apiLanguage = languageMapping[editorLanguage];

    // Create the request body using qs.stringify
    const data = qs.stringify({
      'code': code,
      'language': apiLanguage, // Assuming Python as the default language
      'input': code_input // Optional: Add any input required for the code
    });

    // Configure Axios request
    const config = {
      method: 'post',
      url: 'https://api.codex.jaagrav.in',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      data: data
    };

    // Make the request using Axios
    const response = await axios(config);

    // Log the response
    console.log('Code Execution Result:', response.data);

    // Optionally, store the response in localStorage
    if (response.data.error != "") {
    localStorage.setItem('current_code_error', JSON.stringify(response.data.error));
    localStorage.setItem('current_code_output', JSON.stringify(response.data.output));
    localStorage.setItem('real_error', JSON.stringify(response.data.error));
    } else {
    localStorage.setItem('current_code_error', JSON.stringify(response.data.output));
    localStorage.setItem('current_code_output', JSON.stringify(response.data.output));
    localStorage.setItem('real_error', JSON.stringify(response.data.error));
    }

  } catch (error) {
    // Handle errors
    console.error('Error during code execution:', error);
  } finally {
    // Perform any final actions, like hiding a spinner
    console.log('Finished code execution');
  }
};

</script>
<template>
  <div>
    <div class="bg-light py-3">
      <div class="container">
        <div class="row">
          <div class="col-md-12 mb-0">
            <router-link to="/">Home</router-link>
            <span class="mx-2 mb-0">/</span>
            <strong class="text-black">Lab Assignment</strong>
            <span class="mx-2 mb-0">/</span>
            <strong class="text-black" v-if="codingqs">{{ codingqs.title }}</strong>
          </div>
        </div>
      </div>
    </div>

    <div class="site-section">
      <div class="container" v-if="codingqs">
        <div class="row">
          <!-- Lab Assignment Details -->
          <div class="col-md-12">
            <h2 class="text-black h5 mb-3">{{ codingqs.title }}</h2>
            <p class="text-muted">
              This Lab Assignment belongs to the course:
              <strong>
                <router-link :to="'/course/' + codingqs.course.id">{{ codingqs.course.title }}</router-link>
              </strong>
            </p>
            <p class="text-muted">Created on: {{ formatDate(codingqs.created_at) }}</p>

            <div class="mb-4">
              <h5>{{ codingqs.title }}</h5>
              <p class="font-weight-bold">{{ codingqs.description }}</p>
            </div>
            <div class="mb-4">
              <p class="font-weight-bold">Example Input: {{ codingqs.ex_input }}</p>
              <p class="font-weight-bold">Example Output: {{ codingqs.ex_output }}</p>
            </div>
          </div>

          <!-- Code Editor and Output Section -->
          <div class="col-md-12">
            <div class="code-editor-container mb-4">
              <h5 style="color: white; margin-bottom: 20px;">Write Your Code Here:</h5>
              <code-editor @lang="getLanguage" :languages="[['python', 'Python'], ['javascript', 'JS'], ['java', 'Java'], ['cpp', 'C++'], ['c', 'C'], ['go', 'GoLang'], ['csharp', 'C#']]" width="100%" height="400px" :theme="selectedTheme" v-model="userCode" />
            </div>

            <div class="mb-3">
              <label for="theme-select" class="text-black">Select Theme:</label>
              <select class="form-control" v-model="selectedTheme" id="theme-select">
                <option v-for="theme in themes" :key="theme" :value="theme">{{ theme }}</option>
              </select>
            </div>

            <!-- Submit Button -->
            <button class="btn btn-primary mt-3" @click="compileCode">Run Code</button>

            <!-- Code Output and Error Section -->
            <div class="row mt-5">
              <div class="col-md-12">
                <h5 class="text-black mb-3">Code Output</h5>
                <div class="output-container p-3 mb-4" style="border-left: 4px solid #28a745; background-color: #eafaf1; color: #28a745;">
                  <div v-if="output">
                    <strong>Output:</strong>
                    <pre>{{ output }}</pre>
                  </div>
                  <div v-if="!output">
                    <p>No output to display.</p>
                  </div>
                </div>
                <h5 class="text-black mb-3">Code Error</h5>
                <div class="output-container p-3 mb-4" style="border-left: 4px solid #dc3545; background-color: #fceaea; color: #dc3545;">
                  <div v-if="error">
                    <strong>Error:</strong>
                    <pre>{{ error }}</pre>
                  </div>
                  <div v-if="!error">
                    <p>No Error to display.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="isLoading">
        <p>Loading Lab Assignment details...</p>
      </div>
      <div v-else>
        <p>Error loading Lab. Please try again later.</p>
      </div>
    </div>

    <FooterItem />
  </div>
</template>


<script>
import FooterItem from '../components/FooterItem.vue';
import fetchUtil from '../FetchUtil.js';
import store from '../store';
import { RouterLink } from 'vue-router';
import CodeEditor from "simple-code-editor";
import * as hljs from 'highlight.js';

export default {
  components: {
    FooterItem,
    RouterLink,
    CodeEditor,
  },
  data() {
    return {
      codingqs: null,
      codingqsId: this.$route.params.id,
      selectedAnswers: {},
      codingqsSubmitted: false,
      codingqsResult: null,
      isLoading: true, // Add isLoading flag
      current_lang: null,
      userCode: `print("Hello, World!")`,
      output: null,
      error: null,
      selectedTheme: 'gradient-dark', // Default theme
      themes: [
        'github', 'github-dark', 'gradient-dark', 'hybrid', 'androidstudio',
        'arduino-light', 'arta', 'ascetic', 'atom-one-dark',
         'atom-one-light', 'brown-paper', 'codepen-embed'
      ],
      
    };
  },
  mounted() {
    this.fetchCodeData();
    this.updateErrorAndOutput();
    this.interval = setInterval(this.updateErrorAndOutput, 1000);
  },
  beforeUnmount() {
    // Clear the interval when the component is destroyed
    clearInterval(this.interval);
  },
  watch: {
    userCode(newCode) {
      localStorage.setItem('current_code', newCode); // Update localStorage whenever userCode changes
    },
  },
  methods: {
    updateErrorAndOutput() {
      const error = JSON.parse(localStorage.getItem('real_error'));
      const output = JSON.parse(localStorage.getItem('current_code_output'));

      // Update the local data properties
      if (error !== this.error && error !== "") {
        this.error = error;
      } else if (error == "") {
        this.error = null;
      }

      if (output !== this.output) {
        this.output = output;
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString();
    },
    getLanguage(lang) {
      this.current_lang=lang
      localStorage.setItem('current_lang', lang);
      console.log("The current language is: " + lang);
    },
    async fetchCodeData() {
      this.isLoading = true; // Set isLoading to true while fetching
      try {
        const response = await fetchUtil({
          endpoint: `codingqs/${this.codingqsId}`,
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
          user_id: store.state.currentUser,
        });
        this.codingqs = response;

        localStorage.setItem('code_input', response.ex_input);

        this.userCode=`#code to ${response.description} 
print("Hello, World!")`;
      } catch (error) {
        console.error('Error fetching quiz details:', error);
      } finally {
        this.isLoading = false; // Set isLoading to false regardless of outcome
      }
    },
    handleSubmit() {
      console.log('Submitted code:', this.userCode);
      // Perform any other actions like sending the code to the server
    },
  },
};
</script>

<style scoped>
/* Left column styling */
h2 {
  font-size: 1.75rem;
}

.output-container {
  border-radius: 5px;
  min-height: 100px;
}

pre {
  margin: 0;
  font-family: 'Courier New', Courier, monospace;
}


p {
  margin-bottom: 0.75rem;
}

.font-weight-bold {
  font-weight: bold;
}

/* Right column: code editor */
.code-editor-container {
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 4px;
  background-color: #1A1D1C;
}

/* Larger size for the code editor */
code-editor {
  width: 100%;
  height: 300px;
}

/* Submit button styling */
.btn-primary {
  width: 100%;
}
</style>
