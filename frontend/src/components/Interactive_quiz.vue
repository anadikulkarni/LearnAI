<template>
  <aside :class="['quiz_sidebar', { 'is-expanded': is_q_expanded }]">
    <div class="sidebar-content">
      <div class="menu-toggle-wrap">
        <button class="menu-toggle" @click="toggleSidebar">
          <span class="icon-close"></span>
        </button>
      </div>
      <div class="quiz-card">
        <div class="header-wrap">
          <h3>Quiz</h3>
          <button class="generate-btn" @click="generateQuestions">Generate</button>
        </div>
        <div class="quiz-questions">
          <div v-if="loading" class="loading-spinner">
            <div class="spinner"></div>
          </div>
          <form v-if="!loading && questions.length > 0" @submit.prevent="submitQuiz">
            <div v-for="(question, index) in questions" :key="index" class="question">
              <label :for="'question' + index">{{ question.question }}</label>
              <div class="options-grid">
                <button
                  v-for="(option, optIndex) in question.options"
                  :key="optIndex"
                  type="button"
                  class="option-btn"
                  :class="{ 'selected': selectedAnswers[`question${index}`] === option }"
                  @click="selectOption(`question${index}`, option)"
                >
                  {{ option }}
                </button>
              </div>
            </div>
            <button type="submit" class="submit-btn">Submit</button>
          </form>
          <div v-if="score !== null" class="score">
            <h4>Your Score: {{ score }} out of {{ questions.length }}</h4>
          </div>
        </div>
      </div>
    </div>
  </aside>
  <div v-if="is_q_expanded" class="overlay" @click="toggleSidebar"></div>
</template>

<script setup>
import { ref } from 'vue';

const is_q_expanded = ref(localStorage.getItem("is_q_expanded") === "true");
const score = ref(null);
const selectedAnswers = ref({});
const questions = ref([]);
const loading = ref(false); // Add this line

const toggleSidebar = () => {
  is_q_expanded.value = !is_q_expanded.value;
  localStorage.setItem("is_q_expanded", is_q_expanded.value);
};

const selectOption = (question, answer) => {
  selectedAnswers.value[question] = answer;
};

const submitQuiz = () => {
  let userScore = 0;

  // Check answers
  questions.value.forEach((q, index) => {
    if (selectedAnswers.value[`question${index}`] === q.options[q.correct_option_index]) {
      userScore++;
    }
  });

  score.value = userScore;
};

const generateQuestions = async () => {
  loading.value = true; // Show the spinner
  try {
    let videoId = localStorage.getItem('video_id') || 'JL_grPUnXzY';
    let currentCourseId = localStorage.getItem('current_course_id') || '1';

    const transcriptResponse = await fetch(`http://127.0.0.1:5000/api/videos/${videoId}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    });

    if (!transcriptResponse.ok) throw new Error('Failed to fetch transcript');

    const transcriptData = await transcriptResponse.json();
    const transcript = transcriptData.title;

    const response = await fetch('http://127.0.0.1:5000/api/llm/interactive_quizzes', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ lecture_content: transcript })
    });

    const data = await response.json();
    questions.value = data.quizzes;
  } catch (error) {
    console.error('Error generating questions:', error);
  } finally {
    loading.value = false; // Hide the spinner
  }
};
</script>

<style lang="scss" scoped>
.header-wrap {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.generate-btn {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;

  &:hover {
    background-color: #0056b3;
  }
}

.quiz_sidebar {
  position: fixed;
  bottom: 0;
  left: 0;
  height: 75%;
  width: 500px;
  background-color: #333;
  color: #fff;
  z-index: 1000; /* Ensure it's above the overlay */
  transition: transform 0.3s ease-in-out;
  transform: translateX(-100%);
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.5);

  &.is-expanded {
   transform: translateX(0);
  }

  .sidebar-content {
    padding: 1rem;
    height: 100%; /* Full height of the sidebar */

    .menu-toggle-wrap {
      display: flex;
      justify-content: flex-end;

      .menu-toggle {
        background-color: transparent;
        border: none;
        color: #fff;
        cursor: pointer;
        font-size: 16px;
      }
    }

    .quiz-card {
      background-color: #222;
      padding: 1rem;
      border-radius: 8px;
      height: calc(100% - 2rem); /* Full height minus padding */
      overflow-y: auto; /* Make the quiz card scrollable */
      position: relative; /* Needed for positioning the spinner */

      .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;

        h3 {
          margin: 0;
        }

        .generate-btn {
          background-color: #28a745;
          color: #fff;
          border: none;
          padding: 0.5rem 1rem;
          border-radius: 4px;
          cursor: pointer;
          font-size: 16px;

          &:hover {
            background-color: #218838;
          }
        }
      }

      .quiz-questions {
        display: flex;
        flex-direction: column;

        form {
          display: flex;
          flex-direction: column;

          .question {
            margin-bottom: 1rem;

            label {
              display: block;
              margin-bottom: 0.5rem;
            }

            .options-grid {
              display: grid;
              grid-template-columns: repeat(2, 1fr);
              gap: 0.5rem;

              .option-btn {
                background-color: black;
                color: #fff;
                border: none;
                padding: 0.5rem;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
                text-align: center;
                transition: background-color 0.3s;

                &.selected {
                  background-color: #007bff;
                }

                &:hover {
                  background-color: #0056b3;
                }
              }
            }
          }

          .submit-btn {
            background-color: #007bff;
            color: #fff;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 1rem;

            &:hover {
              background-color: #0056b3;
            }
          }
        }

        .score {
          margin-top: 1rem;
          color: #ffeb3b;
          font-size: 16px;
          font-weight: bold;
        }
      }

      .loading-spinner {
        position: absolute;
        top: 50%;
        left: 45%;
        transform: translate(-50%, -50%);
        width: 10%;
        height: 10%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1100; /* Ensure it's above the quiz content */
      }

      .spinner {
        border: 8px solid #f3f3f3; /* Light grey */
        border-top: 8px solid #007bff; /* Blue */
        border-radius: 50%;
        width: 5px;
        height: 5px;
        animation: spin 1s linear infinite;
      }

      @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
    }
  }
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5); /* Semi-transparent background */
  z-index: 900; /* Lower than sidebar and spinner */
  display: none; /* Hide by default */
}

</style>