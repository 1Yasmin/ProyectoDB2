from sqlListener import sqlListener
from databaseManager import databaseManager

dbManager = databaseManager()

class sqlProcessingListener(sqlListener):
	def __init__(self):
		#self.db = db
            pass

	def enterParse(self,ctx):
		pass
		#print 'Parsing'
		
	def exitUse_database_stmt(self, ctx):
                dbManager.useDatabase(ctx.database_name().getText());	               

	def exitCreate_database_stmt(self, ctx):
		print 'Creando DB'
		# Llamar a clase dbManager para que cree la bd
		
		dbManager.createDatabase(ctx.database_name().getText());
		
		#pdb.set_trace()
	
	def exitShow_databases_stmt(self, ctx):
		dbManager.showDatabase();
		
	def exitCreate_table_stmt(self, ctx):
		dbManager.createTable(ctx.table_name().getText(), ctx.colum_def().getText());
		