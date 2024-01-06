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


{{- define "devopschart.core.labels" -}}
app.kubernetes.io/name: {{ include "devopschart.fullname" . }}
app.kubernetes.io/component: core
{{- end }}

{{- define "devopschart.core.selectorLabels" -}}
app.kubernetes.io/name: {{ include "devopschart.fullname" . }}
app.kubernetes.io/component: core
{{- end }}


{{- define "devopschart.pg.labels" -}}
app.kubernetes.io/name: {{ include "devopschart.fullname" . }}
app.kubernetes.io/component: pg
{{- end }}

{{- define "devopschart.pg.selectorLabels" -}}
app.kubernetes.io/name: {{ include "devopschart.fullname" . }}
app.kubernetes.io/component: pg
{{- end }}


{{- define "devopschart.migrations.labels" -}}
app.kubernetes.io/name: {{ include "devopschart.fullname" . }}
app.kubernetes.io/component: migrations
{{- end }}

{{- define "devopschart.migrations.selectorLabels" -}}
app.kubernetes.io/name: {{ include "devopschart.fullname" . }}
app.kubernetes.io/component: migrations
{{- end }}

