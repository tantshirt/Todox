/**
 * Label types
 */

export interface Label {
  id: string;
  name: string;
  owner_id: string;
  created_at: string;
}

export interface LabelCreate {
  name: string;
}

export interface LabelUpdate {
  name: string;
}
