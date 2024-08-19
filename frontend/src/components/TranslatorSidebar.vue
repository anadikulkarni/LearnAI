<template>
  <aside :class="['translate_sidebar', { 'is_t_expanded': is_t_expanded }]">
    <div class="sidebar-content">
      <div class="menu-toggle-wrap">
        <button class="menu-toggle" @click="ToggleMenu">
          <span class="icon-close"></span>
        </button>
      </div>
      <div class="translate-card">
        <h3>Translate Text</h3>
        <div class="translation-form">
          <textarea v-model="textToTranslate" placeholder="Enter text to translate..." rows="5"></textarea>
          <!-- Dropdown list for selecting the target language -->
          <select v-model="targetLanguage" class="dropdown">
            <option v-for="(name, code) in languages" :key="code" :value="code">
              {{ name }}
            </option>
          </select>
          <button @click="translateText" class="button">Translate</button>
        </div>
        <div class="translation-output">
          <h4>Translated Text</h4>
          <textarea :value="translatedText" readonly></textarea>
        </div>
      </div>
    </div>
  </aside>
  <div class="overlay" @click="ToggleMenu"></div>
</template>

<script setup>
import { ref } from 'vue';
import { EventBus } from '../utils/eventBus.js';

const is_t_expanded = ref(localStorage.getItem("is_t_expanded") === "true");
const textToTranslate = ref('');
const targetLanguage = ref('');
const translatedText = ref('');

// Mapping language codes to full names
const languages = ref({
  fr: "French",
  es: "Spanish",
  en: "English",
  zh: "Chinese",
  hi: "Hindi",
  it: "Italian",
  ja: "Japanese",
  kn: "Kannada",
  ml: "Malayalam",
  ta: "Tamil",
  te: "Telugu"
});

const ToggleMenu = () => {
  is_t_expanded.value = !is_t_expanded.value;
  localStorage.setItem("is_t_expanded", is_t_expanded.value);
};

const translateText = async () => {
  try {
    EventBus.$emit('show-spinner');
    
    const response = await fetch('http://127.0.0.1:5000/api/translations', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: textToTranslate.value, language: targetLanguage.value })
    });

    if (!response.ok) throw new Error('Failed to fetch translation');

    const data = await response.json();
    translatedText.value = data.content;
  } catch (error) {
    console.error('Error:', error);
  } finally {
    EventBus.$emit('hide-spinner');
  }
};
</script>

<style lang="scss" scoped>
.translate_sidebar {
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

  &.is_t_expanded {
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

    .translate-card {
      background-color: black;
      padding: 1rem;
      border-radius: 8px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
      margin: 1rem 0;
      display: flex;
      flex-direction: column;
      flex-grow: 1; /* Allows the card to expand to fill the available space */

      h3 {
        margin: 0 0 1rem;
      }

      .translation-form {
        display: flex;
        flex-direction: column;
        gap: 1rem;

        textarea,
        input,
        .dropdown {
          border: 1px solid #ccc;
          border-radius: 8px;
          padding: 0.5rem;
          background: #fff;
          color: #000;
        }

        textarea {
          resize: none;
        }

        .dropdown {
          padding: 0.5rem;
          background: white;
          color: black;
        }

        .button {
          background-color: var(--primary);
          color: var(--light);
          border: none;
          padding: 0.75rem;
          text-align: center;
          cursor: pointer;
          border-radius: 4px;
          transition: background-color 0.3s ease-in-out;

          &:hover {
            background-color: var(--primary-dark);
          }
        }
      }

      .translation-output {
        margin-top: 1rem;
        flex-grow: 1; /* Allows the output box to grow within the card */
        display: flex;
        flex-direction: column;

        h4 {
          margin: 0 0 0.5rem;
        }

        textarea {
          width: 100%;
          height: 100%; /* Takes up all the available space */
          flex-grow: 1;
          font-size: 12px;
          resize: none;
        }
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
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s ease-in-out;

  &.is_t_expanded + .translate_sidebar {
    opacity: 1;
    visibility: visible;
  }
}
</style>
