<template>
  <aside :class="['sidebar', { 'is-expanded': is_expanded }]">
    <div class="sidebar-content">
      <div class="menu-toggle-wrap">
        <button class="menu-toggle" @click="ToggleMenu">
          <span class="icon-close"></span>
        </button>
      </div>
      <ChatBox />
      <div class="llm-card">
          <button @click="postSummary" class="button">Summarize Lecture</button>
          <button @click="postFeedback" class="button">Code Error Feedback</button>
          <button @click="postQuiz" class="button">Quiz on Lecture</button>
          <button @click="postTranslate" class="button">Translate Lecture Transcript</button>
          <button @click="postAnalyzeCode" class="button">Analyze Coding Style</button>
          <button @click="postDiscussionPrompts" class="button">Discussion Prompts for Lecture</button>
          <button @click="postRecommendCourses" class="button">Recommend Courses</button>
          <button @click="postPersonalizedFeedback" class="button">Personalized Feedback</button>
      </div>
    </div>
  </aside>
  <div class="overlay" @click="ToggleMenu"></div>

  <!-- Prompt Container -->
  <div v-if="showPrompt" class="llm_prompt-container">
    <p>{{ promptMessage }}</p>
    <input v-model="userInput" type="text" placeholder="Enter your response..." />
    <div class="llm_button-container">
      <button @click="submitResponse">Submit</button>
      <button @click="cancelResponse">Cancel</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { EventBus } from '../utils/eventBus.js';
import ChatBox from '../components/ChatBox.vue';

const is_expanded = ref(localStorage.getItem("is_expanded") === "true");
const showPrompt = ref(false);
const promptMessage = ref('');
const userInput = ref('');

const welcomeMessage = async () => {
  try{
    EventBus.$emit('new-message', {
    from: 'chatGpt',
    data: "hello, I'm your AI Learning assistant, Quick note: If no lecture, quiz or code is selected, I'll generate a random sample for you :)"
  });
  } catch (error) {
    console.error('Error:', error);
  }
};

onMounted(() => {
  welcomeMessage();
});

const ToggleMenu = () => {
  is_expanded.value = !is_expanded.value;
  localStorage.setItem("is_expanded", is_expanded.value);
};

const submitResponse = () => {
  showPrompt.value = false;
};

const cancelResponse = () => {
  showPrompt.value = false;
};

const getUserResponse = async (message) => {
  return new Promise((resolve) => {
    // Create a prompt dialog or input field
    const userResponse = prompt(message); // Using prompt for simplicity

    // Store the response in localStorage
    if (userResponse) {
      localStorage.setItem('target_language', userResponse);
    }

    // Resolve the promise with the user input
    resolve(userResponse);
  });
};

// Summarize Lecture
const postSummary = async () => {
  try {
    // Show spinner
    EventBus.$emit('show-spinner');

    let videoId = localStorage.getItem('video_id') || 'JL_grPUnXzY';
    let courseId = localStorage.getItem('current_course_id') || '1';

    const transcriptResponse = await fetch(`http://127.0.0.1:5000/api/transcript/${videoId}?course_id=${courseId}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    });

    if (!transcriptResponse.ok) throw new Error('Failed to fetch transcript');

    const transcriptData = await transcriptResponse.json();
    const transcript = transcriptData.transcript;

    EventBus.$emit('user-message', { from: 'user', data: "Create a summary of the lecture" });

    const summaryResponse = await fetch('http://127.0.0.1:5000/api/llm/summary', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ transcript })
    });

    if (!summaryResponse.ok) throw new Error('Failed to fetch summary');

    const summaryData = await summaryResponse.json();
    const summary = summaryData.summary;

    EventBus.$emit('new-message', { from: 'chatGpt', data: summary });
  } catch (error) {
    console.error('Error:', error);
  } finally {
    // Hide spinner
    EventBus.$emit('hide-spinner');
  }
};

// Feedback
const postFeedback = async () => {
  try {
	EventBus.$emit('show-spinner');

    let code = localStorage.getItem('current_code') || `def example_function(x): return x * 2; print(example_function(5))`;
    let error = localStorage.getItem('current_code_error') || "TypeError: unsupported operand type(s) for *: 'str' and 'int'";

    EventBus.$emit('user-message', { from: 'user', data: "Requesting feedback on code" });

    const response = await fetch('http://127.0.0.1:5000/api/llm/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code, error })
    });

    if (!response.ok) throw new Error('Failed to fetch feedback');

    const data = await response.json();
    EventBus.$emit('new-message', { from: 'chatGpt', data: data.feedback });
  } catch (error) {
    console.error('Error:', error);
  }finally {
    // Hide spinner
    EventBus.$emit('hide-spinner');
  }
};

// Quiz
const postQuiz = async () => {
  try {
	EventBus.$emit('show-spinner');

    let videoId = localStorage.getItem('video_id') || 'JL_grPUnXzY';
    let currentCourseId = localStorage.getItem('current_course_id') || '1';

    const transcriptResponse = await fetch(`http://127.0.0.1:5000/api/videos/${videoId}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    });

    if (!transcriptResponse.ok) throw new Error('Failed to fetch transcript');

    const transcriptData = await transcriptResponse.json();
    const transcript = transcriptData.title;

    EventBus.$emit('user-message', { from: 'user', data: "Requesting quiz questions based on the lecture" });

    const quizResponse = await fetch('http://127.0.0.1:5000/api/llm/quiz', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic: transcript })
    });

    if (!quizResponse.ok) throw new Error('Failed to fetch quiz questions');

    const quizData = await quizResponse.json();
    const questions = quizData.questions;

    EventBus.$emit('new-message', { from: 'chatGpt', data: questions });
  } catch (error) {
    console.error('Error:', error);
  }finally {
    // Hide spinner
    EventBus.$emit('hide-spinner');
  }
};

// Translate
const postTranslate = async () => {
  try {
	EventBus.$emit('show-spinner');
    // Prompt user for target language and store it in localStorage
    const target_language = await getUserResponse("Please enter the target language for translation:");

    // Check if input is provided
    if (!target_language) {
      console.error('No language provided');
      return;
    }

    // Output or use the target_language as needed
    console.log('Target Language:', target_language);

	let videoId = localStorage.getItem('video_id') || 'JL_grPUnXzY';
    let currentCourseId = localStorage.getItem('current_course_id') || '1';

    // Continue with API requests or other logic
    // Example: Making an API call
    const transcriptResponse = await fetch(`http://127.0.0.1:5000/api/transcript/${videoId}?course_id=${currentCourseId}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    });

    if (!transcriptResponse.ok) throw new Error('Failed to fetch transcript');

    const transcriptData = await transcriptResponse.json();
    const transcript = transcriptData.transcript;

    EventBus.$emit('user-message', { from: 'user', data: `Requesting translation of the transcript to ${target_language}` });

    const translateResponse = await fetch('http://127.0.0.1:5000/api/llm/translate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ transcript: transcript, language: target_language })
    });

    if (!translateResponse.ok) throw new Error('Failed to fetch translation');

    const translateData = await translateResponse.json();
    const translation = translateData.translation;

    EventBus.$emit('new-message', { from: 'chatGpt', data: translation });

  } catch (error) {
    console.error('Error:', error);
  }finally {
    // Hide spinner
    EventBus.$emit('hide-spinner');
  }
};

// Analyze Code
const postAnalyzeCode = async () => {
  try {
	EventBus.$emit('show-spinner');
    let code = localStorage.getItem('current_code') || `def example_function(x): return x * 2; print(example_function(5))`;

    EventBus.$emit('user-message', { from: 'user', data: "Analyzing code in terms of industry standards!" });

    const response = await fetch('http://127.0.0.1:5000/api/llm/analyze_code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code:code })
    });

    if (!response.ok) throw new Error('Failed to fetch code analysis');

    const data = await response.json();
    EventBus.$emit('new-message', { from: 'chatGpt', data: data.analysis });
  } catch (error) {
    console.error('Error:', error);
  }finally {
    // Hide spinner
    EventBus.$emit('hide-spinner');
  }
};

// Discussion Prompts
const postDiscussionPrompts = async () => {
  try {
	EventBus.$emit('show-spinner');
    let videoId = localStorage.getItem('video_id') || 'JL_grPUnXzY';
    let currentCourseId = localStorage.getItem('current_course_id') || '1';

    EventBus.$emit('user-message', { from: 'user', data: "Fetching discussion prompts" });

	const transcriptResponse = await fetch(`http://127.0.0.1:5000/api/transcript/${videoId}?course_id=${currentCourseId}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    });

    if (!transcriptResponse.ok) throw new Error('Failed to fetch transcript');

    const transcriptData = await transcriptResponse.json();
    const transcript = transcriptData.transcript;

    const response = await fetch(`http://127.0.0.1:5000/api/llm/discussion_prompts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic: transcript })
    });

    if (!response.ok) throw new Error('Failed to fetch discussion prompts');

    const data = await response.json();
    EventBus.$emit('new-message', { from: 'chatGpt', data: data.prompts });
  } catch (error) {
    console.error('Error:', error);
  }finally {
    // Hide spinner
    EventBus.$emit('hide-spinner');
  }
};

// Recommend Courses
const postRecommendCourses = async () => {
  try {
	EventBus.$emit('show-spinner');
	let user_id = localStorage.getItem('user_id') || 2 ;

    EventBus.$emit('user-message', { from: 'user', data: "Requesting course recommendations for you" });

    const response = await fetch(`http://127.0.0.1:5000/api/llm/recommend_courses`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: user_id })
    });

    if (!response.ok) throw new Error('Failed to fetch course recommendations');

    const data = await response.json();
    EventBus.$emit('new-message', { from: 'chatGpt', data: data.recommendations });
  } catch (error) {
    console.error('Error:', error);
  }finally {
    // Hide spinner
    EventBus.$emit('hide-spinner');
  }
};

// Personalized Feedback
const postPersonalizedFeedback = async () => {
  try {
	EventBus.$emit('show-spinner');
    const defaultQuizResults = {
  1: { score: 85, date: '2024-08-01' },
  2: { score: 90, date: '2024-08-02' },
  3: { score: 75, date: '2024-08-03' },
  4: { score: 88, date: '2024-08-04' },
  5: { score: 92, date: '2024-08-05' },
  courseName: 'Data Science'
};

const defaultAssignmentResults = {
  1: { grade: 'A', submissionDate: '2024-07-30' },
  2: { grade: 'B', submissionDate: '2024-07-31' },
  3: { grade: 'A', submissionDate: '2024-08-01' },
  4: { grade: 'C', submissionDate: '2024-08-02' },
  5: { grade: 'B', submissionDate: '2024-08-03' },
  courseName: 'Data Science'
};

// Retrieve values from localStorage or use default values
let quizResults = JSON.parse(localStorage.getItem('quiz_results')) || defaultQuizResults;
let assignmentResults = JSON.parse(localStorage.getItem('assignment_results')) || defaultAssignmentResults;

    EventBus.$emit('user-message', { from: 'user', data: "Requesting personalized feedback" });

    const response = await fetch(`http://127.0.0.1:5000/api/llm/personalized_feedback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ quiz_results: quizResults, assignment_results:assignmentResults })
    });

    if (!response.ok) throw new Error('Failed to fetch personalized feedback');

    const data = await response.json();
    EventBus.$emit('new-message', { from: 'chatGpt', data: data.feedback });
  } catch (error) {
    console.error('Error:', error);
  }finally {
    // Hide spinner
    EventBus.$emit('hide-spinner');
  }
};
</script>

<style lang="scss" scoped>
.sidebar {
  position: fixed;
  bottom: 0;
  left: 0;
  height: 75%;
  width: 800px;
  background-color: var(--dark);
  color: var(--light);
  z-index: 1000;
  transition: transform 0.3s ease-in-out;
  transform: translateX(-100%);
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.5);

  &.is-expanded {
    transform: translateX(0);
  }

  .sidebar-content {
    display: flex;
    flex-direction: column;
    padding: 1rem;
    height: 100%;
    box-sizing: border-box;

    .menu-toggle-wrap {
      display: flex;
      justify-content: flex-end;
      margin-bottom: 1rem;

      .menu-toggle {
        background-color: transparent;
        border: none;
        cursor: pointer;
        font-size: 16px;
        color: white;
        padding: 8px;
        display: flex;
        align-items: center;
        justify-content: center;

        .icon-close {
          color: white;
        }

        &:hover .icon-close {
          color: #f00;
        }
      }
    }

// .llm-card {
//   background-color: black;
//   top: 0;
//   padding: 1rem;
//   border-radius: 8px;
//   box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
//   margin: 1rem 0;

//   .dropdown {
//     position: relative;
//     display: inline-block;

//     .dropdown-button {
//       background-color: #1877F2;
//       color: var(--light);
//       border: none;
//       padding: 0.75rem 1rem;
//       text-align: center;
//       cursor: pointer;
//       border-radius: 4px;
//       transition: background-color 0.3s ease-in-out;

//       &:hover {
//         background-color: var(--primary-dark);
//       }
//     }

//     .dropdown-content {
//       display: block;
//       position: absolute;
//       background-color: #1877F2;
//       min-width: 160px;
//       box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
//       z-index: 1;
//       border-radius: 4px;
//       padding: 0.5rem 0;

//       .button {
//         background-color: #1877F2;
//         color: #1877F2;
//         border: none;
//         padding: 0.75rem 1rem;
//         text-align: left;
//         width: 100%;
//         cursor: pointer;
//         border-radius: 4px;
//         transition: background-color 0.3s ease-in-out;

//         &:hover {
//           background-color: var(--primary-light);
//         }
//       }
//     }
//   }
// }
.llm-card {
  background-color: black;
  top: 0;
  padding: 0.5rem;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  margin: 0.5rem 0;
}

.llm-card .button {
  background-color: #1877F2;
  color: var(--light);
  border: none;
  padding: 0.1rem 0.25rem; /* Reduced padding to make the button smaller */
  text-align: center;
  cursor: pointer;
  border-radius: 2px;
  transition: background-color 0.3s ease-in-out;
  margin-right: 0.5rem; /* Adds spacing between buttons */
  margin-bottom: 0.5rem; /* Adds spacing below the button */
}

.llm-card .button:last-child {
  margin-right: 0; /* Removes extra margin on the last button */
}

.llm-card .button:hover {
  background-color: var(--primary-dark);
}
  }
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s ease-in-out;

  &.is-expanded + .sidebar {
    opacity: 1;
    visibility: visible;
  }
}

.llm_prompt-container {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 20px;
  background: white;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  z-index: 1001;
}

.llm_prompt-container p {
  margin: 0 0 10px;
}

.llm_prompt-container input {
  width: calc(100% - 22px);
  padding: 8px;
  margin-bottom: 10px;
}

.llm_button-container {
  display: flex;
  justify-content: space-between;
}

.llm_button-container button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.llm_button-container button:hover {
  opacity: 0.8;
}

.llm_button-container button:first-of-type {
  background-color: #007bff;
  color: white;
}

.llm_button-container button:last-of-type {
  background-color: #ccc;
}
</style>
