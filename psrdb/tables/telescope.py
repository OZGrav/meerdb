from psrdb.graphql_table import GraphQLTable
from psrdb.graphql_query import graphql_query_factory


class Telescope(GraphQLTable):
    def __init__(self, client, token):
        GraphQLTable.__init__(self, client, token)
        self.record_name = "telescope"

        self.field_names = ["id", "name"]

    def list(self, id=None, name=None):
        """Return a list of records matching the id and/or the name."""
        filters = [
            {"field": "name", "value": name},
        ]
        return GraphQLTable.list_graphql(self, self.table_name, filters, [], self.field_names)

    def create(self, name):
        self.mutation_name = "createTelescope"
        self.mutation = """
        mutation ($name: String!) {
            createTelescope(input: {
                name: $name,
                }) {
                telescope {
                    id
                }
            }
        }
        """
        self.variables = {
            "name": name,
        }
        return self.mutation_graphql()

    def update(self, id, name):
        self.mutation_name = "updateTelescope"
        self.mutation = """
        mutation ($id: Int!, $name: String!) {
            updateTelescope(id: $id, input: {
                name: $name,
                }) {
                telescope {
                    id,
                    name
                }
            }
        }
        """
        self.variables = {
            "id": id,
            "name": name,
        }
        return self.mutation_graphql()

    def delete(self, id):
        self.mutation_name = "deleteTelescope"
        self.mutation = """
        mutation ($id: Int!) {
            deleteTelescope(id: $id) {
                ok
            }
        }
        """
        self.variables = {
            "id": id,
        }
        return self.mutation_graphql()

    def process(self, args):
        """Parse the arguments collected by the CLI."""
        self.print_stdout = True
        if args.subcommand == "list":
            return self.list(args.id, args.name)
        elif args.subcommand == "create":
            return self.create(args.name)
        elif args.subcommand == "update":
            return self.update(args.id, args.name)
        elif args.subcommand == "delete":
            return self.delete(args.id)
        else:
            raise RuntimeError(args.subcommand + " command is not implemented")

    @classmethod
    def get_name(cls):
        return "telescope"

    @classmethod
    def get_description(cls):
        return "A telescope defined by a name"

    @classmethod
    def get_parsers(cls):
        """Returns the default parser for this model"""
        parser = GraphQLTable.get_default_parser("Telescope model parser")
        cls.configure_parsers(parser)
        return parser

    @classmethod
    def configure_parsers(cls, parser):
        """Add sub-parsers for each of the valid commands."""
        # create the parser for the "list" command
        parser.set_defaults(command=cls.get_name())
        subs = parser.add_subparsers(dest="subcommand")
        subs.required = True

        parser_list = subs.add_parser("list", help="list existing telescopes")
        parser_list.add_argument("--id", metavar="ID", type=int, help="list telescopes matching the id [int]")
        parser_list.add_argument("--name", metavar="NAME", type=str, help="list telescopes matching the name [str]")

        # create the parser for the "create" command
        parser_create = subs.add_parser("create", help="create a new telescope")
        parser_create.add_argument("name", metavar="NAME", type=str, help="name of the telescope [str]")

        # create the parser for the "update" command
        parser_update = subs.add_parser("update", help="update an existing telescope")
        parser_update.add_argument("id", metavar="ID", type=int, help="id of an existing telescope [int]")
        parser_update.add_argument("name", metavar="NAME", type=str, help="name of the telescope [str]")

        parser_delete = subs.add_parser("delete", help="delete an existing telescope")
        parser_delete.add_argument("id", metavar="ID", type=int, help="id of an existing telescope [int]")


if __name__ == "__main__":
    parser = Telescope.get_parsers()
    args = parser.parse_args()

    from psrdb.graphql_client import GraphQLClient

    client = GraphQLClient(args.url, args.very_verbose)

    t = Telescope(client, args.url, args.token)
    t.process(args)