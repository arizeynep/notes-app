"""
Frontend integration tests using Playwright.
Tests the real frontend + backend interaction.
"""
import uuid
import pytest
from playwright.sync_api import expect, Page
import subprocess
import time
import os

from app.domain import note


# Fixtures for starting the backend server
@pytest.fixture(scope="session")
def backend_server():
    """Start the backend server for testing."""
    env = os.environ.copy()
    env['DATABASE_URL'] = 'sqlite:///./test_frontend.db'

    # This deletes the test database per session, but I also want to ensure it's clean before each test, 
    # so I'll add a fixture for that as well
    if os.path.exists('test_frontend.db'):
        os.remove('test_frontend.db')

    process = subprocess.Popen(
        ['python', '-m', 'uvicorn', 'main:app', '--host', '127.0.0.1', '--port', '8000'],
        cwd='/home/moro/Zeynep/projects/notes-app',
        env=env
    )
    time.sleep(2)  # Wait for server to start
    yield process
    process.terminate()
    process.wait()


@pytest.mark.frontend
class TestNotesApp:
    """Test suite for the Notes App frontend."""

    @pytest.fixture(autouse=True)
    def setup(self, page, backend_server):
        """Setup for each test - navigate to the app."""
        page.goto('http://localhost:5173')  # Vite dev server
        yield

    def reset_db():
        """Delete the test database before each test."""
        if os.path.exists('test_frontend.db'):
            os.remove('test_frontend.db')

    def test_app_loads(self, page):
        """Test that the app loads successfully."""
        expect(page.locator('h1')).to_contain_text('Notes')
        expect(page.locator('.new-btn')).to_be_visible()

    def test_create_note(self, page):
        """Test creating a new note."""
        # Create a new note 
        page.click('.new-btn')
        
        # Title and content inputs should be visible
        title_input = page.locator('.title-input')
        content_input = page.locator('.content-input')
        expect(title_input).to_be_visible()
        expect(content_input).to_be_visible()
        
        # Fill in the note details
        title_input.fill('Test Note')
        content_input.fill('This is test content')
        
        # Click the "Add note" button
        page.click('.primary')
        
        # The form should disappear after adding
        expect(title_input).not_to_be_visible()
        
        # The note should appear in the list
        note = page.locator('.note-item', has_text='Test Note').first
        expect(note).to_be_visible()

    def test_edit_note(self, page):
        """Test creating and editing a note using the provided template."""
        # Create a new note to edit
        page.click('.new-btn')
        
        # Fill the adding form
        page.locator('.title-input').fill('Original Title')
        page.locator('.content-input').fill('Original Content')
        page.locator('.adding-wrapper .primary').click()  # Click 'Add note'
        
        # Wait for the new note to appear in the list
        note_row = page.locator('.note-item', has_text='Original Title')
        note_row.wait_for(state="visible", timeout=5000)
        
        # Start editing the note
        note_row.locator('.start-edit').click()
        
        # Wait for the editing form to appear
        edit_title = page.locator('.editing-wrapper .edit-title-input')
        edit_content = page.locator('.editing-wrapper .edit-content-input')
        edit_title.wait_for(state="visible", timeout=5000)
        edit_content.wait_for(state="visible", timeout=5000)
        
        # Verify the form is populated with the original note details
        expect(edit_title).to_have_value('Original Title')
        expect(edit_content).to_have_value('Original Content')
        
        # Update the note details
        edit_title.fill('Updated Title')
        edit_content.fill('Updated Content')
        page.locator('.editing-wrapper .edit-form-actions .primary').click()  # Click 'Save'
        
        # Verify the updated note appears 
        updated_note = page.locator('.note-item', has_text='Updated Title')
        updated_note.wait_for(state="visible", timeout=5000)


    def test_delete_note(self, page):
        """Test deleting a note."""
        # Create a note first
        page.click('.new-btn')
        page.locator('.title-input').fill('Note to Delete')
        page.locator('.content-input').fill('Delete me')
        page.click('.primary')
        
        # Wait for note to appear
        page.wait_for_selector('button:has-text("Note to Delete")')
        
        # Click delete button
        note_row = page.locator('.note-item', has_text='Note to Delete')
        note_row.locator('.delete-note').click()

        expect(note_row).to_have_count(0)
        
        # The note should be removed from the list
        note = page.locator('.note-item', has_text='Note to Delete').first
        expect(note).not_to_be_visible()

    def test_cancel_adding(self, page):
        """Test canceling the add form."""
        # Create a new note 
        page.click('.new-btn')
        
        # Fill in some content
        page.locator('.title-input').fill('Unsaved Note')
        page.locator('.content-input').fill('This will be discarded')
        
        # Click cancel
        page.locator('button:has-text("Cancel")').first.click()
        
        # The form should disappear
        expect(page.locator('.title-input')).not_to_be_visible()

    def test_unsaved_changes_popup_add_to_add(self, page):
        """Test unsaved changes popup when switching from adding to adding."""
        # Create a new note and fill in some content
        page.click('.new-btn')
        page.locator('.title-input').fill('First Note')
        
        # Click "New" again
        page.click('.new-btn')
        
        # Popup should appear
        expect(page.locator('.overlay')).to_be_visible()
        expect(page.locator('p:has-text("unsaved changes")')).to_be_visible()
        
        # Click "Discard"
        page.locator('button:has-text("Discard")').first.click()
        
        # Popup should disappear
        expect(page.locator('.overlay')).not_to_be_visible()

    def test_multiple_notes(self, page):
        """Test creating multiple notes."""
        notes_data = [
            {'title': f'Note 1 {uuid.uuid4()}', 'content': 'Content 1'},
            {'title': f'Note 2 {uuid.uuid4()}', 'content': 'Content 2'},
            {'title': f'Note 3 {uuid.uuid4()}', 'content': 'Content 3'},
        ]

        for note in notes_data:
            page.click('.new-btn')
            page.locator('.title-input').fill(note['title'])
            page.locator('.content-input').fill(note['content'])
            page.click('.primary')

            note_row = page.locator('.note-item', has_text=note["title"])
            expect(note_row).to_be_visible()

