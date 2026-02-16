<template>
  <div class="container" @mouseup="stopResize" @mousemove="resize" @mouseleave="stopResize">

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

    <div class="divider" @mousedown="startResize"></div>

    <div class="right" ref="rightPanel" :style="{ width: rightWidth + '%' }">
      <div v-if="adding" class="adding-wrapper">
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
      <div v-if="editing">
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
    // await pauses execution of this function until the fetch Promise resolves
    // fetch(...) starts an HTTP request to the URL ${API}/notes
    async fetchNotes() {
      const res = await fetch(`${API}/notes`)
      this.notes = await res.json()
    },

    async createNote() {
      this.adding = true;
      if (!this.newTitle) return
      const res = await fetch(`${API}/notes`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ title: this.newTitle, content: this.newContent }) // Converts a JavaScript object into a JSON-formatted string
      })
      
      // res.ok is a shortcut property on the Response object that is true when the HTTP status code is in the 200–299 range
      if (res.ok) {
        this.newTitle = ''
        this.newContent = ''
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
    },

    startEdit(n) {
      this.editing = true
      this.editId = n.id
      this.editTitle = n.title
      this.editContent = n.content
    },

    cancelEdit() {
      this.editing = false
      this.editId = null
    },

    cancelAdding() {
      this.adding = false
      this.editId = null
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

