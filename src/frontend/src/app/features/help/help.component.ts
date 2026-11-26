import { Component } from '@angular/core';

interface ReasonGroup {
  id: number;
  range: string;
  label: string;
  desc: string;
}

interface Reason {
  code: number;
  label: string;
  group: number;
}

/**
 * Page Guide / Aide (contenu statique).
 * Explique le fonctionnement de l'app, les 4 groupes de motifs d'absence
 * (tels que définis dans le backend : app/ml/preprocessing.py → reason_to_group)
 * et le détail des 28 codes CIM-10 du jeu de données "Absenteeism at Work".
 */
@Component({
  selector: 'app-help',
  standalone: true,
  imports: [],
  templateUrl: './help.component.html',
  styleUrl: './help.component.css',
})
export class HelpComponent {
  /** Les 4 groupes, alignés sur reason_to_group() côté backend. */
  groups: ReasonGroup[] = [
    { id: 1, range: '1 – 14', label: 'Maladies', desc: 'Pathologies déclarées (infectieuses, tumeurs, troubles mentaux, système nerveux, circulatoire, respiratoire…).' },
    { id: 2, range: '15 – 17', label: 'Grossesse / périnatal', desc: 'Grossesse et accouchement, période périnatale, malformations congénitales.' },
    { id: 3, range: '18 – 21', label: 'Causes externes', desc: 'Lésions, empoisonnements, causes externes et symptômes non classés ailleurs.' },
    { id: 4, range: '22 – 28 et 0', label: 'Motifs légers', desc: 'Consultations, suivis médicaux, examens, don du sang… et code 0 (inconnu / non renseigné).' },
  ];

  /** Les 29 codes de motif (0 à 28) avec leur intitulé CIM-10 et leur groupe. */
  reasons: Reason[] = [
    { code: 0, label: 'Inconnu / non renseigné', group: 4 },
    { code: 1, label: 'Maladies infectieuses et parasitaires', group: 1 },
    { code: 2, label: 'Tumeurs (néoplasmes)', group: 1 },
    { code: 3, label: 'Maladies du sang et troubles immunitaires', group: 1 },
    { code: 4, label: 'Maladies endocriniennes, nutritionnelles et métaboliques', group: 1 },
    { code: 5, label: 'Troubles mentaux et du comportement', group: 1 },
    { code: 6, label: 'Maladies du système nerveux', group: 1 },
    { code: 7, label: "Maladies de l'œil et de ses annexes", group: 1 },
    { code: 8, label: "Maladies de l'oreille", group: 1 },
    { code: 9, label: "Maladies de l'appareil circulatoire", group: 1 },
    { code: 10, label: "Maladies de l'appareil respiratoire", group: 1 },
    { code: 11, label: "Maladies de l'appareil digestif", group: 1 },
    { code: 12, label: 'Maladies de la peau et du tissu sous-cutané', group: 1 },
    { code: 13, label: 'Maladies ostéo-articulaires, muscles et tissu conjonctif', group: 1 },
    { code: 14, label: "Maladies de l'appareil génito-urinaire", group: 1 },
    { code: 15, label: 'Grossesse, accouchement et puerpéralité', group: 2 },
    { code: 16, label: 'Affections de la période périnatale', group: 2 },
    { code: 17, label: 'Malformations congénitales et anomalies chromosomiques', group: 2 },
    { code: 18, label: 'Symptômes et résultats cliniques/labo anormaux non classés', group: 3 },
    { code: 19, label: 'Lésions, empoisonnements et causes externes', group: 3 },
    { code: 20, label: 'Causes externes de morbidité et de mortalité', group: 3 },
    { code: 21, label: "Facteurs influant sur l'état de santé / recours aux soins", group: 3 },
    { code: 22, label: 'Suivi médical (patient follow-up)', group: 4 },
    { code: 23, label: 'Consultation médicale', group: 4 },
    { code: 24, label: 'Don du sang', group: 4 },
    { code: 25, label: 'Examen de laboratoire', group: 4 },
    { code: 26, label: 'Absence injustifiée', group: 4 },
    { code: 27, label: 'Physiothérapie / kinésithérapie', group: 4 },
    { code: 28, label: 'Consultation dentaire', group: 4 },
  ];
}
