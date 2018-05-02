from sqlListener import sqlListener
from sqlParser import sqlParser
from databaseManager import databaseManager
import pdb

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
        # Llamar a clase dbManager para que cree la bd
        
        dbManager.createDatabase(ctx.database_name().getText());
        
        #pdb.set_trace()
    
    def exitShow_databases_stmt(self, ctx):
        dbManager.showDatabase();
        
    def exitCreate_table_stmt(self, ctx):
        #pdb.set_trace()

        dbManager.createTable(
            ctx.table_name().getText(),
            ctx.column_def(None),
            ctx.table_constraint(None)
        );
        
    def exitInsert_stmt(self, ctx):
        dbManager.insertStmt(ctx.table_name().getText(), ctx.expr(), ctx.column_name());
        
    def exitDrop_database_stmt(self, ctx):
        dbManager.dropDatabase(ctx.database_name().getText());
        
    def exitAlterRenameTo (self, ctx):
        print(ctx)
        dbManager.alterTable(sqlParser().alter_table_specific_stmt(self, ctx).new_table_name());
        
    def exitAlter_table_stmt(self, ctx):
        self.exitAlterRenameTo();
    
    def exitAlter_database_stmt(self, ctx):
        dbManager.alterDatabase(ctx.database_name().getText(), ctx.new_database_name().getText());
    
    def exitShow_columns_stmt(self,ctx):
        dbManager.showColumnsFrom(ctx.table_name().getText());
        
    def exitInsert_stmt(self,ctx):
        dbManager.insertInto(ctx.table_name().getText(), ctx.expr(),ctx.K_VALUES());
        
    def exitDrop_table_stmt(self,ctx):
        dbManager.dropTable(ctx.table_name().getText());
        
    def exitShow_tables_stmt(self,ctx):
        dbManager.showTables();