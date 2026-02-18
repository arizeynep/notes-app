<template>
  <div class="container" @mouseup="stopResize" @mousemove="resize" @mouseleave="stopResize">

    <!-- LEFT PANEL -->
    <div class="left" ref="leftPanel" :style="{ width: leftWidth + '%' }">
      <div class="notes-header">
        <h1>Notes</h1>
        <button class="new-btn" @click="createNote">+ New</button>
      </div>
      <div class="notes-list" v-for="n in notes" :key="n.id">
        <div class="note-item">
          <button class="start-edit" @click="startEdit(n)">{{n.title}}</button>
          <button class="delete-note" @click="deleteNote(n.id)">Delete</button>
        </div>
      </div>
    </div>

    <!-- DIVIDER -->
    <div class="divider" @mousedown="startResize"></div>

    <!-- RIGHT PANEL -->
    <div class="right" ref="rightPanel" :style="{ width: rightWidth + '%' }">
      <!-- Show this form when adding a new note -->
      <div v-if="adding && showPopup != 2 || showPopup == 0" class="adding-wrapper">
        <form class="note-form" @submit.prevent="createNote">
          <div class="notes-content">
            <input class="title-input" v-model="newTitle" placeholder="Title" />
            <textarea class="content-input" v-model="newContent" placeholder="Content"></textarea>
          </div>
          <div class="form-actions">
            <button type="button" @click="addNote" class="primary">Add note</button>
            <button type="button" @click="cancelAdding">Cancel</button>
          </div>
        </form>
      </div>

      <!-- Show this form when editing an existing note -->
      <div v-if="editing && showPopup != 3 || showPopup == 1" class="editing-wrapper">
          <form class="edit-note-form" @submit.prevent="startEdit">
          <div class="edit-notes-content">
            <input class="edit-title-input" v-model="editTitle"/>
            <textarea class="edit-content-input" v-model="editContent"></textarea>
          </div>
          <div class="edit-form-actions">
            <button type="button" class="primary" @click="updateNote">Save</button>
            <button type="button" @click="cancelEdit">Cancel</button>
          </div>
        </form>

      </div>
    </div>

    <!-- Popup for when there are unsaved changes while switching from creating a note to adding another -->
    <div v-if="showPopup == 0" class="overlay">
      <div class="popup">
        <p>You have unsaved changes. Do you want to discard them?</p>
        <div class="popup-actions">
          <button class="primary" @click="showPopup = -1; cancelAdding(); createNote();">Discard</button>
          <button type="resume" @click="showPopup = -1;">Continue</button>
        </div>
        </div>
    </div>

    <!-- Popup for when there are unsaved changes while switching from editing a note to editing another -->
    <div v-if="showPopup == 1" class="overlay">
      <div class="popup">
        <p>You have unsaved changes. Do you want to discard them?</p>
        <div class="popup-actions">
          <button class="primary" @click="showPopup = -1; cancelEdit(); startEdit(currentNote);">Discard</button>
          <button type="resume" @click="showPopup = -1;">Continue</button>
        </div>
        </div>
    </div>

    <!-- Popup for when there are unsaved changes while switching from editing to adding -->
    <div v-if="showPopup == 2" class="overlay">
      <div class="popup">
        <p>You have unsaved changes. Do you want to discard them?</p>
        <div class="popup-actions">
          <button class="primary" @click="showPopup = -1; cancelEdit(); createNote();">Discard</button>
          <button type="resume" @click="showPopup = -1; adding = false;">Continue</button>
        </div>
        </div>
    </div>

      <!-- Popup for when there are unsaved changes while switching from adding to editing -->
      <div v-if="showPopup == 3" class="overlay">
        <div class="popup">
          <p>You have unsaved changes. Do you want to discard them?</p>
          <div class="popup-actions">
            <button class="primary" @click="showPopup = -1; cancelAdding(); startEdit(currentNote);">Discard</button>
            <button type="resume" @click="showPopup = -1; editing = false;">Continue</button>
          </div>
        </div>
    </div>

  </div>
</template>

<script>
import appLogic from './appLogic.js'

export default appLogic
</script>

