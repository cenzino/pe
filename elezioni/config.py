# -*- coding: utf-8 -*-

RICERCATORI = 'Ricercatori'
RILEVATORI = 'Rilevatori'
EMITTENTI = 'Emittenti'

DEFAULT_SYSTEM_GROUPS = (
    RICERCATORI,
    RILEVATORI,
    EMITTENTI
)

CAN_VIEW_REPORTS = ("can_view_reports", "Può visualizzare i reports")
CAN_VIEW_PROJECTIONS = ("can_view_projections", "Può visualizzare le proiezioni")
CAN_UPDATE_VOTES = ("can_update_votes", "Può aggiornare i voti")

DEFAULT_SYSTEM_PERMISSIONS = (
    CAN_VIEW_REPORTS,
    CAN_VIEW_PROJECTIONS,
    CAN_UPDATE_VOTES
)

DEFAULT_SYSTEM_PERMISSIONS_NAME = ['elezioni.%s' % (p[0]) for p in DEFAULT_SYSTEM_PERMISSIONS]

def get_default_system_permissions_set():
    return ['elezioni.%s' % (p[0]) for p in DEFAULT_SYSTEM_PERMISSIONS]


DEFAULT_SYSTEM_GROUPS_PERMISSIONS = {
  RICERCATORI: (
      CAN_VIEW_REPORTS[0],
      CAN_VIEW_PROJECTIONS[0],
  ),
  RILEVATORI: (
      CAN_UPDATE_VOTES[0],
  ),
  EMITTENTI: (
      CAN_VIEW_PROJECTIONS[0],
  ),
}

UPLOAD_IMG_PATH = 'upload/images/'