from yapsy.IPlugin import IPlugin

enabled = False


def greet_user(name='Incognito'):
    '''RPC command to greet a user. See the _server_plugin_example grammar for
       how to use on the client side via voice.'''
    print 'Hello user %s!' % name


# def paste(text='default'):
#     '''RPC command to greet a user. See the _server_plugin_example grammar for
#        how to use on the client side via voice.'''
#     print 'it worked: %s' % text


class ExamplePlugin(IPlugin):
    def register_rpcs(self, server):
        server.register_function(greet_user)
        # server.register_function(paste)
