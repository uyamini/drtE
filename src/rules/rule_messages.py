def user_message(cell_str, col, reason):
    """Returns a user-friendly message for why the cell is dirty.
    
    Args:
        cell_str (str) : the string version of the cell
        col (Column) : a container class with information about the cell's column
        reason (RuleBaseClass) : a class type representing the reason why the cell is dirty

    Returns:
        message (str) : a readable string for why the cell is dirty
    """
    return reason.message(cell_str, col)
    