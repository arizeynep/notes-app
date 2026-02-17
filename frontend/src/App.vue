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
      <div v-if="adding && !showPopupEdit" class="adding-wrapper">
        <form class="note-form" @submit.prevent="createNote">
          <div class="notes-content">
            <input class="title-input" v-model="newTitle" placeholder="Title" />
            <textarea class="content-input" v-model="newContent" placeholder="Content"></textarea>
          </div>
          <div class="form-actions">
            <button type="submit" class="primary">Add note</button>
            <button type="button" @click="cancelAdding">Cancel</button>
          </div>
        </form>
      </div>

      <!-- Show this form when editing an existing note -->
      <div v-if="editing && !showPopupAdd" class="editing-wrapper">
          <form class="edit-note-form" @submit.prevent="startEdit">
          <div class="edit-notes-content">
            <input class="edit-title-input" v-model="editTitle"/>
            <textarea class="edit-content-input" v-model="editContent"></textarea>
          </div>
          <div class="edit-form-actions">
            <button type="submit" class="primary" @click="updateNote">Save</button>
            <button type="button" @click="cancelEdit">Cancel</button>
          </div>
        </form>

      </div>
    </div>

    <!-- Popup for when there are unsaved changes while switching from editing to adding -->
    <div v-if="showPopupEdit" class="overlay">
      <div class="popup">
        <p>You have unsaved changes. Do you want to discard them?</p>
        <div class="popup-actions">
          <button class="primary" @click="showPopupEdit = false; cancelEdit(); createNote();">Discard</button>
          <button type="resume" @click="showPopupEdit = false; adding = false;">Continue</button>
        </div>
        </div>
    </div>

      <!-- Popup for when there are unsaved changes while switching from adding to editing -->
      <div v-if="showPopupAdd" class="overlay">
        <div class="popup">
          <p>You have unsaved changes. Do you want to discard them?</p>
          <div class="popup-actions">
            <button class="primary" @click="showPopupAdd = false; cancelAdding(); startEdit(currentNote);">Discard</button>
            <button type="resume" @click="showPopupAdd = false; editing = false;">Continue</button>
          </div>
        </div>
    </div>

  </div>
</template>

<script>

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default {
  data() {
    return {
      notes: [],
      newTitle: '',
      newContent: '',
      adding: false,
      editing: false,
      editId: null,
      editTitle: '',
      editContent: '',
      isResizing: false,
      showPopupEdit: false,
      showPopupAdd: false,
      currentNote: null,
      leftWidth: 50,
      rightWidth: 50
    }
  },

  // When the component loads, it automatically calls fetchNotes() to load all saved notes from backend
  created() {
    this.fetchNotes()
  },

  methods: {
    // async means the function can use await inside it to pause until Promises resolve
    // fetch(...) starts an HTTP request to the URL ${API}/notes
    async fetchNotes() {
      const res = await fetch(`${API}/notes`)
      this.notes = await res.json()
    },

    async createNote() {
      this.adding = true;

      // If uou're currently editing a note and click "New", check for unsaved changes before switching to the add form
      if(this.editing) {
          if(this.currentNote.title !== this.editTitle || this.currentNote.content !== this.editContent) {
            this.showPopupEdit = true
          }
          else {
            this.cancelEdit()
          }
        return
      }

      if (!this.newTitle) return
      const res = await fetch(`${API}/notes`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ title: this.newTitle, content: this.newContent }) // Converts a JavaScript object into a JSON-formatted string
      })
      
      
      // res.ok is a shortcut property on the Response object that is true when the HTTP status code is in the 200–299 range
      if (res.ok) {
        this.cancelAdding()
        await this.fetchNotes()
      } else {
        alert('Failed to create note')
      }
    },

    async deleteNote(id) {
      const res = await fetch(`${API}/notes/${id}`, { method: 'DELETE' })
      
      // 204 is the special "No Content" status — commonly used to indicate a successful deletion where the server returns no body
      if (res.status === 204) this.fetchNotes()
      this.editing = false
    },

    startEdit(n) {
      this.editing = true
      this.currentNote = n
      this.editId = n.id
      this.editTitle = n.title
      this.editContent = n.content

      // If you're currently adding a new note and click on an existing note to edit, check for unsaved changes before switching to the edit form
      if(this.adding) {
        if(this.newTitle !== '' || this.newContent !== '') {
          this.showPopupAdd = true
        }
        else {
          this.cancelAdding()
        }
        return
      }
    },

    cancelEdit() {
      this.editing = false
      this.editId = null
    },

    cancelAdding() {
      this.adding = false
      this.newTitle = ''
      this.newContent = ''
    },


    async updateNote() {
      const res = await fetch(`${API}/notes/${this.editId}`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ title: this.editTitle, content: this.editContent })
      })

      if (res.ok) {
        this.cancelEdit()
        await this.fetchNotes()
      } else {
        alert('Update failed')
      }
    },

    startResize() {
      this.isResizing = true
    },

    stopResize() {
      this.isResizing = false
    },

    resize(e) {
      if (!this.isResizing) return
      const container = e.currentTarget
      const newLeftWidth = (e.clientX / container.clientWidth) * 100
      if (newLeftWidth > 20 && newLeftWidth < 80) {
        this.leftWidth = newLeftWidth
        this.rightWidth = 100 - newLeftWidth
      }
    }
  }
}
</script>

