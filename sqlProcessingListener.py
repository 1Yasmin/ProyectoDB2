from sqlListener import sqlListener
from databaseManager import databaseManager

dbManager = databaseManager()

class sqlProcessingListener(sqlListener):
	def __init__(self):
		#self.db = db
                print 'holi'

	def enterParse(self,ctx):
		print 'Parsing'
		
	def exitUse_database_stmt(self, ctx):
                dbManager.useDatabase(ctx.database_name().getText());	               

	def exitCreate_database_stmt(self, ctx):
		print 'Creando DB'
		# Llamar a clase dbManager para que cree la bd
		
		dbManager.createDatabase(ctx.database_name().getText());
		
		#pdb.set_trace()
		
		
