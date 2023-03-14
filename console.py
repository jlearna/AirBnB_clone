#!/usr/bin/python3
""" This module defines a class 'HBNBCommand """
import cmd
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the entry point of the command interpreter """
    prompt = "(hbnb) "
    __classes = ["BaseModel",
                 "User",
                 "State",
                 "City",
                 "Amenity",
                 "Place",
                 "Review"
                 ]

    def do_quit(self, arg):
        """Quit command to exit the program
        """
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program
        """
        return True

    def emptyline(self):
        """ Method called when an empty line is
            entered in response to the prompt
            """
        return

    def do_create(self, arg):
        """ Creates a new instance of BaseModel,
            saves it (to the JSON file and prints the id

            Usage: create <class_name>
        """
        args = arg.split()

        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.__classes:
            print("** class doesn't exist **")
        else:
            new_object = eval(f"{args[0]}")()
            print(new_object.id)
        storage.save()

    def do_show(self, arg):
        """ Prints the string representation of
            an instance based on the class name and id

            Usage: show <class_name> <object_id>
        """
        args = arg.split()

        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.__classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif f"{args[0]}.{args[1]}" not in storage.all():
            print("** no instance found **")
        else:
            print(storage.all()[f"{args[0]}.{args[1]}"])

    def do_destroy(self, arg):
        """ Deletes an instance based on the class name and id

            Usage: destroy <class_name><object_id>
        """
        args = arg.split()

        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.__classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif f"{args[0]}.{args[1]}" not in storage.all():
            print("** no instance found **")
        else:
            del storage.all()[f"{args[0]}.{args[1]}"]
        storage.save()

    def do_all(self, arg):
        """ Prints all string representation of all
            instances based or not on the class name

            Usage: all OR all <class_name>
        """
        args = arg.split()

        if len(args) == 0:
            print([str(value) for value in storage.all().values()])
        elif args[0] not in self.__classes:
            print("** class doesn't exist **")
        else:
            m = storage.all().items()
            print([str(v) for k, v in m if k.startswith(arg[0])])

    def do_update(self, arg):
        """ Updates an instance based on the class
            name and is by adding or updating attribute

            Usage: update <class_name> <id> <attr_name> "<attr_value>"
        """
        args = arg.split()

        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.__classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif f"{args[0]}.{args[1]}" not in storage.all():
            print("** no instance found **")
        elif len(args) == 2:
            print("** attribute name missing **")
        elif len(args) == 3:
            print("** value missing **")
        else:
            obj_class = args[0]
            obj_id = args[1]
            obj_key = obj_class + "." + obj_id
            obj = storage.all()[obj_key]

            attr_name = args[2]
            attr_value = args[3]

            if attr_value[0] == '"':
                attr_value = attr_value[1:-1]

            if hasattr(obj, attr_name):
                type_ = type(getattr(obj, attr_name))
                if type_ in [str, float, int]:
                    attr_value = type_(attr_value)
                    setattr(obj, attr_name, attr_value)
            else:
                setattr(obj, attr_name, attr_value)
            storage.save()

    def default(self, arg):
        """ Update your command interpreter to retrieve all
            instances of a class
                Usage: <class_name>.all()

            Update your command interpreter to retrieve
            an instance based on its ID

                Usage: <class_name>.show(<id>)

            Update your command interpreter to destroy an
            instance based on its ID

                Usage: <class_name>.<destroy(<id>)

            Update your command interpreter to update an
            instance based on its ID.

                Usage: <class_name>.update(<id>, <attr_name>, <attr value>)

            Update your command interpreter to update an
            instance based on its ID with a dictionary

                Usage: <class_name>.update(<id>, <dictionary representation>)

        """

        args = arg.split('.')
        if args[0] in self.__classes:
            if args[1] == "all()":
                self.do_all(args[0])
            elif args[1] == "count()":
                list_ = [v for k, v in
                         storage.all().items()
                         if k.startswith(args[0])]
                print(len(list_))
            elif args[1].startswith("show"):
                id_ = args[1].split('"')[1]
                self.do_show(f"{args[0]} {id_}")
            elif args[1].startswith("destroy"):
                id_ = args[1].split('"')[1]
                self.do_destroy(f"{args[0]} {id_}")
            elif args[1].startswith("update"):
                split_ = args[1].split('(')
                split_ = split_[1].split(')')
                if '{' in split_[0]:
                    # If a dictionary is passed
                    split_ = split_[0].split(", {")
                    id_ = split_[0].strip('"')
                    dict_ = '{' + split_[1]
                    dict_ = (eval(dict_))

                    for k, v in dict_.items():
                        self.do_update(f"{args[0]} {id_}"
                                       "{attr_name} {attr_value}")
                else:
                    # If not a dictionary is passed
                    split_ = split_[0].split(', ')
                    id_ = split_[0].strip('"')
                    attr_name = split_[1].strip('"')
                    attr_value = split_[2].strip('"')
                    self.do_update(f"{args[0]} {id_} {attr_name} {attr_value}")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
