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
		dbManager.createTable(ctx.table_name().getText(), ctx.column_def(None));
		
	
	#def exitColumn_constraint(self, ctx):
	#dbManager.columnConstraint(ctx.signed_number().getText(), ctx.literal_value().getText(), ctx.expr().getText());

	def exitTable_constraint(self, ctx):
		dbManager.tableConstraint(ctx.name().getText(), ctx.column_name(), ctx.expr().getText, ctx.foreign_key_clause());
		
	def exitInsert_stmt(self, ctx):
		dbManager.insertStmt(ctx.table_name().getText(), ctx.expr(), ctx.column_name());
		
	def exitDrop_database_stmt(self, ctx):
		dbManager.dropDatabase(ctx.database_name().getText());
		
	def exitAlter_table_stmt(self, ctx):
		dbManager.alterTable(ctx.table_name().getText(),ctx.new_table_name().getText(),ctx.column_def(),ctx.table_constraint(),ctx.column_name(), ctx.name());
	
	def exitAlter_database_stmt(self, ctx):
		dbManager.alterDatabase(ctx.database_name().getText(), ctx.new_database_name().getText());