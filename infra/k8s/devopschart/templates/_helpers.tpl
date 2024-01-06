{{- define "devopschart.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

*/}}
{{- define "devopschart.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}


{{- define "chart.core.labels" -}}
app.kubernetes.io/name: {{ include "devopschart.fullname" . }}
app.kubernetes.io/component: core
{{- end }}

{{- define "chart.core.selectorLabels" -}}
app.kubernetes.io/name: {{ include "devopschart.fullname" . }}
app.kubernetes.io/component: core
{{- end }}


{{- define "chart.pg.labels" -}}
app.kubernetes.io/name: {{ include "devopschart.fullname" . }}
app.kubernetes.io/component: pg
{{- end }}

{{- define "chart.pg.selectorLabels" -}}
app.kubernetes.io/name: {{ include "devopschart.fullname" . }}
app.kubernetes.io/component: pg
{{- end }}


{{- define "chart.migrations.labels" -}}
app.kubernetes.io/name: {{ include "devopschart.fullname" . }}
app.kubernetes.io/component: migrations
{{- end }}

{{- define "chart.migrations.selectorLabels" -}}
app.kubernetes.io/name: {{ include "devopschart.fullname" . }}
app.kubernetes.io/component: migrations
{{- end }}

