from django import forms
from .models import Permuta, Reposicao
from accounts.models import Professor


class PermutaSolicitacaoForm(forms.ModelForm):
    class Meta:
        model = Permuta
        fields = ["data_aula", "professor_substituto", "motivo"]
        labels = {
            "data_aula": "Data da aula a ser permutada",
            "professor_substituto": "Professor substituto",
            "motivo": "Motivo da permuta",
        }
        widgets = {
            "data_aula": forms.DateInput(attrs={"type": "date"}),
            "motivo": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        professor_solicitante = kwargs.pop("professor_solicitante", None)
        super().__init__(*args, **kwargs)

        qs = Professor.objects.all()
        if professor_solicitante is not None:
            qs = qs.exclude(id=professor_solicitante.id)

        self.fields["professor_substituto"].queryset = qs


class ReposicaoForm(forms.ModelForm):
    class Meta:
        model = Reposicao
        fields = ["data_reposicao", "observacao"]
        labels = {
            "data_reposicao": "Data da reposição",
            "observacao": "Observações",
        }
        widgets = {
            "data_reposicao": forms.DateInput(attrs={"type": "date"}),
            "observacao": forms.Textarea(attrs={"rows": 4}),
        }
