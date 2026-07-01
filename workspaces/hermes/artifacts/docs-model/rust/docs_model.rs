use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::collections::BTreeMap;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "kebab-case")]
pub enum DocKind {
    Collection,
    Architecture,
    Adr,
    Spec,
    Brief,
    Workflow,
    Runbook,
    Policy,
    Role,
    Decision,
    Handoff,
    Archive,
    Aar,
    Note,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "kebab-case")]
pub enum Lifecycle {
    Draft,
    Active,
    Paused,
    Archived,
    Superseded,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "kebab-case")]
pub enum Authority {
    Normative,
    Advisory,
    Historical,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct DocNode {
    pub name: String,
    pub path: String,
    pub kind: DocKind,
    pub lifecycle: Lifecycle,
    pub authority: Authority,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    #[serde(default, skip_serializing_if = "BTreeMap::is_empty")]
    pub metadata: BTreeMap<String, Value>,
    #[serde(default)]
    pub children: Vec<DocNode>,
}
