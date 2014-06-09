from JakeBot import Command
import JakeBot


@Command(name="perms", help="Permissions management command", aliases="permissions, perm")
def perms(chat, message, args, sender):
    if len(args) == 0:
        chat.SendMessge("Provide parameters")
        return
    if len(args) < 2:
        chat.SendMessge("Provide a subparam and a user.")
        return
    handle = args[1]
    if args[0] == "add":
        if len(args) < 3:
            chat.SendMessge("Provide a permission to set.")
            return
        JakeBot.add_permission(handle, args[2])
    elif args[0] == "remove":
        if len(args) < 3:
            chat.SendMessge("Provide a permission to remove.")
            return
        JakeBot.remove_permission(handle, args[2])
    elif args[0] == "list":
        temp = ''
        for perm in JakeBot.get_permissions(handle):
            temp += perm + ", "
        temp = temp[:2]
        chat.SendMessage("Permissions: " + temp)
    else:
        chat.SendMessage("Sub parameter not found!")
        return
