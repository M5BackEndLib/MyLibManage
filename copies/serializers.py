from rest_framework import serializers
from .models import Copy, CopyLoan
from datetime import datetime, timedelta


class CopySerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True, source="book.title")

    class Meta:
        model = Copy
        fields = [
            "id",
            "name",
            "book_id",
            "added_in",
            "disponibility",
        ]
        read_only_fields = ["id", "added_in", "book_id", "disponibility"]


class CopyLoanSerializer(serializers.ModelSerializer):
    copy = CopySerializer(read_only=True)

    class Meta:
        model = CopyLoan
        fields = ("id", "loan_in", "returned", "returned_in", "copy")
        read_only_fields = fields

    def create(self, validated_data):
        user = validated_data["user"]
        copy = validated_data["copy"]
        existing_copy_loans = CopyLoan.objects.filter(user=user, returned=False)
        if existing_copy_loans.exists():
            raise serializers.ValidationError("User already has a copy on loan")
        if not copy.disponibility:
            raise serializers.ValidationError("Copy not available for loan")

        # Verificar se existem cópias emprestadas há mais de uma semana
        one_week_ago = datetime.now() - timedelta(days=7)
        overdue_copy_loans = CopyLoan.objects.filter(
            user=user, loan_in__lt=one_week_ago, returned=False
        )
        if overdue_copy_loans.exists():
            user.is_blocked = True
            user.save()

        if user.is_blocked:
            raise serializers.ValidationError({"error": "Este usuário está bloqueado."})

        copy_loan = CopyLoan.objects.create(
            user=user,
            copy=copy,
        )
        copy.disponibility = False
        copy.save()
        return copy_loan
