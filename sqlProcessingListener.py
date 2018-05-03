from sqlListener import sqlListener
from sqlParser import sqlParser
from databaseManager import databaseManager
import pdb

dbManager = databaseManager()


class sqlProcessingListener(sqlListener):
    #tablaActual = ""
    def __init__(self):
        #self.db = db
        pass
        
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
        dbManager.insertInto(ctx.table_name().getText(), ctx.expr(), ctx.column_name());

    def exitDrop_database_stmt(self, ctx):
        dbManager.dropDatabase(ctx.database_name().getText());

    def enterAlter_table_stmt(self, ctx):
        # Opcion 1: Setear la tabla que va a ser modificada
        # pdb.set_trace()
        #dbManager.alterTable(ctx.table_name().getText(), ctx.alter_table_specific_stmt());
        print "Opcion 1: setear tabla a ", ctx.table_name().getText()
        #tablaActual = ctx.table_name().getText()
        dbManager.setCurrentDatabase(ctx.table_name().getText())
        #self.exitAlterRenameTo();

    def exitAlterRenameTo(self, ctx):
        print "Opcion 1: In rename to"
        #print(ctx.new_table_name().getText())
        dbManager.alterRenameTo( ctx.new_table_name().getText())
        # dbManager.alterTable(sqlParser().alter_table_specific_stmt(self, ctx).new_table_name());
        # Opcion 2 evaluar el tipo de ctx.getChild(3)
        # dbManager.setCurrentTable(nombreTabla)

    def exitAlterAddColumn(self, ctx):
        print "Opcion 1: In add column to"
        # dbManager.addColumn(dbManager.setCurrentTable, nuevaColumna, tipoNuevaColumna);
        #print(ctx.column_def().getText())
        dbManager.alterAddColumn( ctx.column_def().getText())

    # Exit a parse tree produced by sqlParser#alterAddConstraint.
    def exitAlterAddConstraint(self, ctx):
        print "Opcion 1: In add constraint"
        #print(ctx.table_constraint().getText())
        dbManager.alterAddConstraint( ctx.table_constraint().getText())

    # Exit a parse tree produced by sqlParser#alterDropColumn.
    def exitAlterDropColumn(self, ctx):
        print "Opcion 1: In drop column"
        #print(ctx.column_name().getText())
        dbManager.alterDropColumn(ctx.column_name().getText())

    # Exit a parse tree produced by sqlParser#alterDropConstraint.
    def exitAlterDropConstraint(self, ctx):
        print "Opcion 1: In drop constraint"
        #print(ctx.name().getText())
        dbManager.alterDropConstraint( ctx.name().getText())





    
    def exitAlter_database_stmt(self, ctx):
        dbManager.alterDatabase(ctx.database_name().getText(), ctx.new_database_name().getText());
    
    def exitShow_columns_stmt(self,ctx):
        dbManager.showColumnsFrom(ctx.table_name().getText());
        
    def exitDrop_table_stmt(self,ctx):
        dbManager.dropTable(ctx.table_name().getText());
        
    def exitShow_tables_stmt(self,ctx):
        dbManager.showTables();
