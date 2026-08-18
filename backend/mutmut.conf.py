import sys

def pre_mutation(context):
    # Skip test files
    if "test" in context.filename:
        context.skip = True
    # Skip certain functions if needed
    pass

def pre_mutate_file(context, file_path):
    # Example: skip migrations
    if "alembic" in file_path or "migrations" in file_path:
        context.skip = True
    pass