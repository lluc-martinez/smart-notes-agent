from sqlmodel import Session, select
from app.db.session import engine
from app.models.db_models import User, Note, ShoppingItem
from app.schemas.llm_schemas import RouterOutput

def get_or_create_user(telegram_id: int, username: str) -> User:
    """Find the user by Telegram ID, or create them if this is their first message."""
    with Session(engine) as session:
        statement = select(User).where(User.telegram_id == telegram_id)
        user = session.exec(statement).first()
        
        if not user:
            user = User(telegram_id=telegram_id, username=username)
            session.add(user)
            session.commit()
            session.refresh(user)
            
        return user

def execute_action(router_output: RouterOutput, telegram_id: int, username: str) -> None:
    """Insert or modify database records according to the AI's intent."""
    user = get_or_create_user(telegram_id, username)

    with Session(engine) as session:
        # --- BLOCK: ADD TO THE LIST ---
        if router_output.intent == "shopping" and router_output.action == "add":
            for item_name in router_output.entities.items:
                if item_name:
                    new_item = ShoppingItem(user_id=user.id, item_name=item_name)
                    session.add(new_item)
            session.commit()

        # --- NEW BLOCK: REMOVE FROM THE LIST ---
        elif router_output.intent == "shopping" and router_output.action == "remove":
            for item_name in router_output.entities.items:
                # Find the item in the database (case-insensitive with ilike)
                statement = select(ShoppingItem).where(
                    ShoppingItem.user_id == user.id,
                    ShoppingItem.is_bought == False,
                    ShoppingItem.item_name.ilike(f"%{item_name}%")
                )
                item_to_remove = session.exec(statement).first()
                
                if item_to_remove:
                    # Mark it as bought
                    item_to_remove.is_bought = True
                    session.add(item_to_remove)
            
            session.commit()

        # --- BLOCK: ADD NOTE ---
        elif router_output.intent == "note" and router_output.action == "add":
            tags_str = ",".join(router_output.entities.tags) if router_output.entities.tags else ""
            new_note = Note(
                user_id=user.id, 
                content=router_output.entities.content, 
                tags=tags_str
            )
            session.add(new_note)
            session.commit()
        
        # Calendar functionality will be added in a future phase
def get_shopping_list(telegram_id: int) -> str:
    """Retrieve the user's active shopping list."""
    with Session(engine) as session:
        statement_user = select(User).where(User.telegram_id == telegram_id)
        user = session.exec(statement_user).first()
        
        if not user:
            return "You are not registered yet. Send me a regular message first."
        
        statement_items = select(ShoppingItem).where(
            ShoppingItem.user_id == user.id,
            ShoppingItem.is_bought == False
        )
        items = session.exec(statement_items).all()
        
        if not items:
            return "🛒 Your shopping list is empty."
        
        text = "🛒 <b>Shopping list:</b>\n\n"
        for item in items:
            text += f"• {item.item_name}\n"
        
        return text

def get_notes_context(telegram_id: int) -> str:
    """
    Retrieves all notes for a specific user to inject as context for the LLM.
    """
    with Session(engine) as session:
        statement_user = select(User).where(User.telegram_id == telegram_id)
        user = session.exec(statement_user).first()
        
        if not user:
            return "No user found in the database."
        
        statement_notes = select(Note).where(Note.user_id == user.id)
        notes = session.exec(statement_notes).all()
        
        if not notes:
            return "The user has no notes saved."
        
        # Format the notes as a clear text list for the LLM to read easily
        context = "Here are the user's saved notes:\n"
        for note in notes:
            context += f"- [Tags: {note.tags}] {note.content}\n"
            
        return context