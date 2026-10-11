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
    """Insert data into the database according to the AI's intent."""
    user = get_or_create_user(telegram_id, username)

    with Session(engine) as session:
        if router_output.intent == "shopping" and router_output.action == "add":
            # Iterate over the items extracted by the LLM
            for item_name in router_output.entities.items:
                if item_name:  # Avoid saving empty strings
                    new_item = ShoppingItem(user_id=user.id, item_name=item_name)
                    session.add(new_item)
            session.commit()

        elif router_output.intent == "note" and router_output.action == "add":
            # Convert the list of tags to a string for easy storage in SQLite
            tags_str = ",".join(router_output.entities.tags) if router_output.entities.tags else ""
            new_note = Note(
                user_id=user.id, 
                content=router_output.entities.content, 
                tags=tags_str
            )
            session.add(new_note)
            session.commit()
        
        # Calendar functionality will be added in a future phase
