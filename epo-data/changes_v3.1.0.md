:doctitle: eProcurement Ontology
:doccode: epo-v3.1.0-prod-002
:page-name: release-notes
:author: NPJ
:authoremail: nicole-anne.paterson-jones@ext.ec.europa.eu
:docdate: June 2023

ifeval::[{epo_latest_version} == {page-component-version}]
:page-aliases: 3.1.0@release-notes.adoc
endif::[]

== *Release notes 3.1.0*

The release of version 3.1.0 and its corresponding technical files can be found link:https://github.com/OP-TED/ePO/tree/v3.1.0[here].


|===
|*Metadata*|*Value*

|Reference ePO version|3.0.1
|Target ePO version|3.1.0
|Authors|Andreea Pasăre, Eugeniu Costetchi
|Date|2022-12-16
|===

* Development of a new module, eOrdering
* The prefix used for the eOrdering module is “epo-ord”
* Included notice systematisation in eNotice module
* Changes to Procurement Object classes and attributes (Procedure, PlannedProcurementPart, Lot)
* Roles hierarchy restructure
* model2owl (uml2owl) updates:
** Combined glossary
** Providing Turtle output files
** Implemented metadata management mechanism
* https://github.com/OP-TED/ePO/issues[GitHub issues] revision and labelling
* GitHub issue fixes for the https://github.com/OP-TED/ePO/milestone/1[Q4 2022 milestone]
* Updates for standard forms mappings - TED-RDF-mapping


== New classes

=== ePO core

* epo:AcquiringParty
* epo:AuxiliaryParty
* epo:LeadBuyer
* epo:OtherEntity
* epo:ProcurementElement
* owl:Thing

== Deleted classes

=== ePO core

* epo:BuyerSideSignatory
* epo:ContractSignatory
* epo:ContractorSideSignatory
* epo:GroupLeader
* epo:InformationProvider
* epo:PrimaryRole
* epo:SecondaryRole
* epo:TertiaryRole

== New controlled vocabularies

=== ePO core

* at-voc:cpvsuppl
* at-voc:review-decision-type (renamed from at-voc:decision-type)
* at-voc:remedy-type (renamed from at-voc:review-remedy-type)
* at-voc-new:evaluation-group-type (changed prefix from epo:)
* at-voc-new:legal-regime (changed prefix from epo:)
* at-voc-new:notification-phases-content-types (changed prefix from epo:)

=== eCatalogue

* at-voc-new:price-type
* at-voc-new:document-type

== Deleted controlled vocabularies

=== ePO core

* espd:eo-role-type

== Changed classes

=== Procurement object package

[cols="1,2,2"]
|===
s|class|added attributes|deleted attributes

|epo:ProcurementElement|epo:hasDescription (moved from epo:ProcurementObject)|
|epo:ProcurementElement|epo:hasTitle (moved from epo:ProcurementObject)|
|epo:ProcurementObject|epo:hasAdditionalInformation (moved from epo:Lot)|
|epo:ProcurementObject|epo:hasRecurrenceDescription (moved from epo:Lot)|
|epo:ProcurementObject|epo:isCoveredByGPA (moved from epo:Lot)|
|epo:ProcurementObject|epo:isRecurrent (moved from epo:Lot)|
|epo:ProcurementObject|epo:isSMESuitable (moved from epo:PlannedProcurementPart)|
|epo:ProcurementObject|epo:isUsingEUFunds (moved from epo:PlannedProcurementPart)|
|===

[cols="1,2,2"]
|===
s|class|added property|deleted property

|epo:AwardDecision|generalisation -> epo:ProcurementElement|generalisation -> epo:ProcurementObject
|epo:Contract|epo:signedByContractor -> epo:Contractor|epo:signedBySignatory -> epo:ContractSignatory
|epo:Contract|generalisation -> epo:ProcurementElement|generalisation -> epo:ProcurementObject
|epo:Contract|epo:signedByBuyer -> epo:Buyer|
|epo:ProcurementObject|epo:hasPurpose -> epo:Purpose (moved from epo:Lot)|
|epo:ProcurementObject|epo:usesChannel -> cv:Channel (moved from epo:PlannedProcurementPart)|
|epo:ProcurementObject|epo:refersToPlannedPart -> epo:PlannedProcurementPart (moved from epo:Procedure)|
|epo:ProcurementObject|epo:hasEstimatedValue -> epo:MonetaryValue (epo:hasEstimatedValue:epo:MonetaryValue|
|epo:ProcurementObject|generalisation -> epo:ProcurementElement|
|epo:ProcurementObject|epo:usesTechnique -> epo:TechniqueUsage (moved from epo:Procedure)|
|epo:ProcurementObject|epo:foreseesContractSpecificTerm -> epo:ContractSpecificTerm (moved from epo:Lot)|
|epo:Purpose|epo:hasMainClassification -> at-voc:cpvsuppl|
|epo:Purpose|epo:hasAdditionalClassification -> at-voc:cpvsuppl|
|epo:ReviewDecision|epo:providesRulingOnRemedy -> at-voc:remedy-type|epo:appliesRemedyType -> at-voc:review-remedy-type
|epo:ReviewObject|generalisation -> epo:ProcurementElement|generalisation -> epo:ProcurementObject
|epo:Tender|generalisation -> epo:ProcurementElement|generalisation -> epo:ProcurementObject
|===

=== Agent package

[cols="1,2,2"]
|===
s|class|added property|deleted property

|cpv:Person|person:placeOfBirth|cpv:placeOfBirth
|cpv:Person|person:placeOfDeath|cpv:placeOfDeath
|org:Organization|cv:registeredAddress -> locn:Address|legal:registeredAddress -> locn:Address
|===


=== Role package

[cols="1,2,2"]
|===
s|class|added property|deleted property

|epo:AcquiringParty|generalisation -> epo:AgentInRole|
|epo:AuxiliaryParty|generalisation -> epo:AgentInRole|
|epo:Awarder|generalisation -> epo:AcquiringParty|generalisation -> epo:PrimaryRole
|epo:BudgetProvider|generalisation -> epo:AcquiringParty|generalisation -> epo:SecondaryRole
|epo:Buyer|generalisation -> epo:AcquiringParty|generalisation -> epo:PrimaryRole
|epo:CatalogueReceiver|generalisation -> epo:AcquiringParty|generalisation -> epo:PrimaryRole
|epo:OfferingParty (renamed from epo:EconomicOperator)|generalisation -> epo:AgentInRole|
|epo:EmploymentInformationProvider|generalisation -> epo:AuxiliaryParty|generalisation -> epo:TertiaryRole
|epo:EnvironmentalProtectionInformationProvider|generalisation -> epo:AuxiliaryParty|generalisation -> epo:TertiaryRole
|epo:LeadBuyer|generalisation -> epo:Buyer|
|epo:Mediator|generalisation -> epo:AcquiringParty|generalisation -> epo:PrimaryRole
|epo:OfflineAccessProvider|generalisation -> epo:AcquiringParty|generalisation -> epo:InformationProvider
|epo:OtherEntity|generalisation -> epo:OfferingParty|
|epo:ParticipationRequestProcessor|generalisation -> epo:AcquiringParty|generalisation -> epo:SecondaryRole
|epo:ParticipationRequestReceiver|generalisation -> epo:AcquiringParty|generalisation -> epo:SecondaryRole
|epo:PaymentExecutor|generalisation -> epo:AcquiringParty|generalisation -> epo:SecondaryRole
|epo:ProcurementProcedureInformationProvider|generalisation -> epo:AcquiringParty|generalisation -> epo:InformationProvider
|epo:ProcurementServiceProvider|generalisation -> epo:AcquiringParty|generalisation -> epo:PrimaryRole
|epo:ReviewProcedureInformationProvider|generalisation -> epo:AcquiringParty|generalisation -> epo:InformationProvider
|epo:ReviewRequester|generalisation -> epo:OfferingParty|generalisation -> epo:PrimaryRole
|epo:Reviewer|generalisation -> epo:AcquiringParty|generalisation -> epo:PrimaryRole
|epo:TaxInformationProvider|generalisation -> epo:AuxiliaryParty|generalisation -> epo:TertiaryRole
|epo:TenderProcessor|generalisation -> epo:AcquiringParty|generalisation -> epo:SecondaryRole
|epo:TenderReceiver|generalisation -> epo:AcquiringParty|generalisation -> epo:SecondaryRole
|===

=== Term package

[cols="1,2,2"]
|===
s|class|added property|deleted property

|epo:AccessTerm|generalisation -> epo:ProcedureSpecificTerm|
|epo:ContractTerm|epo:hasContractNatureType -> at-voc:contract-nature (moved from epo:Purpose)|
|epo:ContractTerm|epo:hasAdditionalContractNature -> at-voc:contract-nature (moved from epo:Purpose)|
|epo:ProcedureTerm|epo:definesInformationProvider -> epo:AuxiliaryParty|
|epo:ProcessPlanningTerm|generalisation -> epo:Term|generalisation -> epo:LotSpecificTerm
|epo:ReviewTerm|generalisation -> epo:LotSpecificTerm|
|===

=== Contextual description package

[cols="1,2,2"]
|===
s|class|added property|deleted property

|epo:LotAwardOutcome|epo:hasRestatedAwardedValue -> epo:MonetaryValue|
|epo:LotAwardOutcome|epo:hasBargainPrice -> epo:MonetaryValue|
|epo:SubmissionStatisticalInformation|epo:summarisesInformationForLotAwardOutcome -> epo:LotAwardOutcome|epo:concernsSubmissionsForLot -> epo:Lot
|epo:TenderAwardOutcome|epo:indicatesAwardOfLotToWinner -> epo:Winner|epo:awardsLotToWinner -> epo:Winner
|===

=== Notice description package

[cols="1,2,2"]
|===
s|class|added attributes|deleted attributes

|epo:ElementConfidentialityDescription|epo:hasInstanceReference|epo:hasClassReference
|===

=== Empirical types package

[cols="1,2,2"]
|===
s|class|added property|deleted property

|owl:Thing|epo:containsModificationsOf -> owl:Thing|
|===

=== eCatalogue module

[cols="1,2,2"]
|===
s|class|added property|deleted property

|epo-cat:Catalogue|epo-cat:isReceivedByCatalogueReceiver -> epo:CatalogueReceiver|
|epo-cat:Catalogue|epo:specifiesSeller -> epo-ord:Seller|
|epo-cat:Catalogue|epo:isIntendedForBuyer -> epo:Buyer|
|epo-cat:ChargeInformation|epo-ord:isSpecificToOrderLine -> epo-ord:OrderLine|
|epo-cat:ChargeInformation|generalisation -> epo-ord:PriceModifierInformation|
|epo-cat:Manufacturer|generalisation -> epo:OfferingParty|generalisation -> epo:SecondaryRole
|epo-cat:Price|epo-cat:hasPriceType: -> at-voc-new:price-type|
|epo-cat:ProductSpecification|epo-cat:hasDocumentType -> at-voc-new:document-type|
|epo-cat:Item|epo:hasBuyerItemID -> epo:Identifier|
|===

include::partial$feedback.adoc[]