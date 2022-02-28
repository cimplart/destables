# Generated from C11.g4 by ANTLR 4.9.3
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .C11Parser import C11Parser
else:
    from C11Parser import C11Parser

# This class defines a complete generic visitor for a parse tree produced by C11Parser.

class C11Visitor(ParseTreeVisitor):

    # Visit a parse tree produced by C11Parser#primaryExpression.
    def visitPrimaryExpression(self, ctx:C11Parser.PrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#genericSelection.
    def visitGenericSelection(self, ctx:C11Parser.GenericSelectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#genericAssocList.
    def visitGenericAssocList(self, ctx:C11Parser.GenericAssocListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#genericAssociation.
    def visitGenericAssociation(self, ctx:C11Parser.GenericAssociationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#postfixExpression.
    def visitPostfixExpression(self, ctx:C11Parser.PostfixExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#argumentExpressionList.
    def visitArgumentExpressionList(self, ctx:C11Parser.ArgumentExpressionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#unaryExpression.
    def visitUnaryExpression(self, ctx:C11Parser.UnaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#unaryOperator.
    def visitUnaryOperator(self, ctx:C11Parser.UnaryOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#castExpression.
    def visitCastExpression(self, ctx:C11Parser.CastExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#multiplicativeExpression.
    def visitMultiplicativeExpression(self, ctx:C11Parser.MultiplicativeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#additiveExpression.
    def visitAdditiveExpression(self, ctx:C11Parser.AdditiveExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#shiftExpression.
    def visitShiftExpression(self, ctx:C11Parser.ShiftExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#relationalExpression.
    def visitRelationalExpression(self, ctx:C11Parser.RelationalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#equalityExpression.
    def visitEqualityExpression(self, ctx:C11Parser.EqualityExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#andExpression.
    def visitAndExpression(self, ctx:C11Parser.AndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#exclusiveOrExpression.
    def visitExclusiveOrExpression(self, ctx:C11Parser.ExclusiveOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#inclusiveOrExpression.
    def visitInclusiveOrExpression(self, ctx:C11Parser.InclusiveOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#logicalAndExpression.
    def visitLogicalAndExpression(self, ctx:C11Parser.LogicalAndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#logicalOrExpression.
    def visitLogicalOrExpression(self, ctx:C11Parser.LogicalOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#conditionalExpression.
    def visitConditionalExpression(self, ctx:C11Parser.ConditionalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#assignmentExpression.
    def visitAssignmentExpression(self, ctx:C11Parser.AssignmentExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#assignmentOperator.
    def visitAssignmentOperator(self, ctx:C11Parser.AssignmentOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#expression.
    def visitExpression(self, ctx:C11Parser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#constantExpression.
    def visitConstantExpression(self, ctx:C11Parser.ConstantExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#declaration.
    def visitDeclaration(self, ctx:C11Parser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#declarationSpecifiers.
    def visitDeclarationSpecifiers(self, ctx:C11Parser.DeclarationSpecifiersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#declarationSpecifiers2.
    def visitDeclarationSpecifiers2(self, ctx:C11Parser.DeclarationSpecifiers2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#declarationSpecifier.
    def visitDeclarationSpecifier(self, ctx:C11Parser.DeclarationSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#initDeclaratorList.
    def visitInitDeclaratorList(self, ctx:C11Parser.InitDeclaratorListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#initDeclarator.
    def visitInitDeclarator(self, ctx:C11Parser.InitDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#storageClassSpecifier.
    def visitStorageClassSpecifier(self, ctx:C11Parser.StorageClassSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#typeSpecifier.
    def visitTypeSpecifier(self, ctx:C11Parser.TypeSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#structOrUnionSpecifier.
    def visitStructOrUnionSpecifier(self, ctx:C11Parser.StructOrUnionSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#structOrUnion.
    def visitStructOrUnion(self, ctx:C11Parser.StructOrUnionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#structDeclarationList.
    def visitStructDeclarationList(self, ctx:C11Parser.StructDeclarationListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#structDeclaration.
    def visitStructDeclaration(self, ctx:C11Parser.StructDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#specifierQualifierList.
    def visitSpecifierQualifierList(self, ctx:C11Parser.SpecifierQualifierListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#structDeclaratorList.
    def visitStructDeclaratorList(self, ctx:C11Parser.StructDeclaratorListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#structDeclarator.
    def visitStructDeclarator(self, ctx:C11Parser.StructDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#enumSpecifier.
    def visitEnumSpecifier(self, ctx:C11Parser.EnumSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#enumeratorList.
    def visitEnumeratorList(self, ctx:C11Parser.EnumeratorListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#enumerator.
    def visitEnumerator(self, ctx:C11Parser.EnumeratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#enumerationConstant.
    def visitEnumerationConstant(self, ctx:C11Parser.EnumerationConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#atomicTypeSpecifier.
    def visitAtomicTypeSpecifier(self, ctx:C11Parser.AtomicTypeSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#typeQualifier.
    def visitTypeQualifier(self, ctx:C11Parser.TypeQualifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#functionSpecifier.
    def visitFunctionSpecifier(self, ctx:C11Parser.FunctionSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#alignmentSpecifier.
    def visitAlignmentSpecifier(self, ctx:C11Parser.AlignmentSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#declarator.
    def visitDeclarator(self, ctx:C11Parser.DeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#directDeclarator.
    def visitDirectDeclarator(self, ctx:C11Parser.DirectDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#gccDeclaratorExtension.
    def visitGccDeclaratorExtension(self, ctx:C11Parser.GccDeclaratorExtensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#gccAttributeSpecifier.
    def visitGccAttributeSpecifier(self, ctx:C11Parser.GccAttributeSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#gccAttributeList.
    def visitGccAttributeList(self, ctx:C11Parser.GccAttributeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#gccAttribute.
    def visitGccAttribute(self, ctx:C11Parser.GccAttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#nestedParenthesesBlock.
    def visitNestedParenthesesBlock(self, ctx:C11Parser.NestedParenthesesBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#pointer.
    def visitPointer(self, ctx:C11Parser.PointerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#typeQualifierList.
    def visitTypeQualifierList(self, ctx:C11Parser.TypeQualifierListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#parameterTypeList.
    def visitParameterTypeList(self, ctx:C11Parser.ParameterTypeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#parameterList.
    def visitParameterList(self, ctx:C11Parser.ParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#parameterDeclaration.
    def visitParameterDeclaration(self, ctx:C11Parser.ParameterDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#identifierList.
    def visitIdentifierList(self, ctx:C11Parser.IdentifierListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#typeName.
    def visitTypeName(self, ctx:C11Parser.TypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#abstractDeclarator.
    def visitAbstractDeclarator(self, ctx:C11Parser.AbstractDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#directAbstractDeclarator.
    def visitDirectAbstractDeclarator(self, ctx:C11Parser.DirectAbstractDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#typedefName.
    def visitTypedefName(self, ctx:C11Parser.TypedefNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#initializer.
    def visitInitializer(self, ctx:C11Parser.InitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#initializerList.
    def visitInitializerList(self, ctx:C11Parser.InitializerListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#designation.
    def visitDesignation(self, ctx:C11Parser.DesignationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#designatorList.
    def visitDesignatorList(self, ctx:C11Parser.DesignatorListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#designator.
    def visitDesignator(self, ctx:C11Parser.DesignatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#staticAssertDeclaration.
    def visitStaticAssertDeclaration(self, ctx:C11Parser.StaticAssertDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#statement.
    def visitStatement(self, ctx:C11Parser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#labeledStatement.
    def visitLabeledStatement(self, ctx:C11Parser.LabeledStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#compoundStatement.
    def visitCompoundStatement(self, ctx:C11Parser.CompoundStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#blockItemList.
    def visitBlockItemList(self, ctx:C11Parser.BlockItemListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#blockItem.
    def visitBlockItem(self, ctx:C11Parser.BlockItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#expressionStatement.
    def visitExpressionStatement(self, ctx:C11Parser.ExpressionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#selectionStatement.
    def visitSelectionStatement(self, ctx:C11Parser.SelectionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#iterationStatement.
    def visitIterationStatement(self, ctx:C11Parser.IterationStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#forCondition.
    def visitForCondition(self, ctx:C11Parser.ForConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#forDeclaration.
    def visitForDeclaration(self, ctx:C11Parser.ForDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#forExpression.
    def visitForExpression(self, ctx:C11Parser.ForExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#jumpStatement.
    def visitJumpStatement(self, ctx:C11Parser.JumpStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#compilationUnit.
    def visitCompilationUnit(self, ctx:C11Parser.CompilationUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#translationUnit.
    def visitTranslationUnit(self, ctx:C11Parser.TranslationUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#externalDeclaration.
    def visitExternalDeclaration(self, ctx:C11Parser.ExternalDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#functionDefinition.
    def visitFunctionDefinition(self, ctx:C11Parser.FunctionDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C11Parser#declarationList.
    def visitDeclarationList(self, ctx:C11Parser.DeclarationListContext):
        return self.visitChildren(ctx)



del C11Parser