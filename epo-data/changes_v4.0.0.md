:doctitle: eProcurement Ontology v4.0.0-rc.2
:page-code: epo-v4.0.0-rc-prod-002
:page-name: release-notes
:author: NPJ
:authoremail: nicole-anne.paterson-jones@ext.ec.europa.eu
:docdate: July 2023

The release candidate v4.0.0-rc.2 and its corresponding technical files can be found link:https://github.com/OP-TED/ePO/tree/v4.0.0-rc.2[here].

== Release notes


|===
|*Metadata*|*Value*

|Reference ePO version|4.0.0-rc.2
|Target ePO version|4.0.0-rc.1
|Authors|Andreea Pasăre
|Date|2023-09-25
|===

= Change notes


== New classes

=== ePO core

* epo:ContextDescription (renamed from epo:ContextSpecificDescription)
* epo:Certificate (moved from ePO Catalogue module)
* epo:CertificationLabel (moved from ePO Catalogue module)
* epo:ChangeInformation (renamed from epo:NoticeChangeInformation)
* epo:Certifier (moved form ePO Catalogue module)

== Deleted classes

=== ePO core

* epo:ContextSpecificDescription (renamed to epo:ContextDescription)
* epo:NoticeChangeInformation (renamed to epo:ChangeInformation)

=== eCatalogue

* epo:Certificate (moved to ePO Core module)
* epo:CertificationLabel (moved to ePO Core module)
* epo:Certifier (moved to ePO Core module)
* epo-cat:CatalogueFragment

== New Controlled Vocabularies

=== ePO core

* at-voc-new:certification-label-type (moved from ePO Catalogue module)

== Deleted Controlled Vocabularies

=== eCatalogue

* at-voc-new:certification-label-type (moved to ePO Core)
* at-voc-new:vat-category


== Changed classes


|===
|*module*|*class*|*added attributes*|*deleted attributes*

|*ePO Core*|org:Organization||epo:hasOrganisationUnitName
||epo:Notice||epo:hasLongTitle
||epo:LotGroup|dct:description|
||epo:LotGroup|dct:title|
||epo:TenderGroup|dct:description|
||epo:TenderGroup|dct:title|
||epo:DesignContestRegimeTerm|epo:hasDescriptionOfPrizes|
||epo:ProcedureTerm|epo:isSubmissionForAllLotsRequired|epo:isSubmissionForAllLotsAllowed
|===



|===
|*module*|*class*|*added property*|*deleted property*

|*ePO core*|org:Organization|org:subOrganizationOf -> org:Organization|
||epo:LotAwardOutcome||epo:hasAwardedEstimatedValue -> epo:MonetaryValue
||epo:LotAwardOutcome||epo:hasFrameworkAgreementEstimatedValue -> epo:MonetaryValue
||epo:NoticeAwardInformation|epo:describesDirectAwardPrenotificationNotice -> epo-not:DirectAwardPrenotificationNotice|epo:describesResultNotice -> epo-not:DirectAwardPrenotificationNotice
||cccev:Evidence|epo:hasValidityPeriod -> epo:Period|
||cccev:Requirement|adms:identifier -> adms:Identifier|
||epo:Certificate||epo:hasValidityPeriod -> epo:Period
||epo:Notice||epo:conformsToSpecificLegalBasis -> at-voc:legal-basis
||epo:LotGroup|epo:hasInternalIdentifier -> adms:Identifier|
||epo:LotGroup|epo:hasEstimatedValue -> epo:MonetaryValue|
||epo:LotGroup|epo:hasLaunchFrameworkAgreementMaximumValue -> epo:MonetaryValue|
||epo:ProcurementObject|epo:hasLaunchFrameworkAgreementMaximumValue -> epo:MonetaryValue|
||epo:TenderGroup|adms:identifier -> adms:Identifier|
||epo:Certifier|generalisation -> epo:AuxiliaryParty|
||epo:JuryMember|epo:playedBy -> cpv:Person|epo:playedBy -> foaf:Person
||epo:OpeningTerm|generalisation -> epo:ProcedureSpecificTerm|
||epo:DesignContestRegimeTerm|generalisation -> epo:ProcedureSpecificTerm|
||epo:FrameworkAgreementTerm||epo:hasLaunchGroupFrameworkAgreementMaximumValue -> epo:MonetaryValue
||epo:FrameworkAgreementTerm||epo:hasLaunchFrameworkAgreementMaximumValue -> epo:MonetaryValue
||epo:ReviewTerm|generalisation -> epo:ProcedureSpecificTerm|
||epo:SubmissionTerm|epo:hasTenderValidityDuration -> epo:Duration|
|*eCatalogue*|epo-cat:CatalogueLine|epo-cat:hasActivityCode -> at-voc-new:activity-code|
||epo-cat:Catalogue|epo-cat:hasActivityCode -> at-voc-new:activity-code|
|*eOrdering*|epo-ord:TaxInformation||epo-cat:hasVATCategory -> at-voc-new:vat-category
|*eContract*|epo-con:ContractAmendment|epo:updatesContractValue -> epo:MonetaryValue|epo:hasRestatedContractValue -> epo:MonetaryValue
|===



== *eProcurement Ontology v4.0.0-rc.1*

The release candidate v4.0.0-rc.1 and its corresponding technical files can be found link:https://github.com/OP-TED/ePO/tree/v4.0.0-rc.1[here].

== Release notes

|===
|*Metadata*|*Value*

|Reference ePO version|3.1.0
|Target ePO version|4.0.0-rc.1
|Authors|Andreea Pasăre, Eugeniu Costetchi
|Date|2023-07-19
|===

* Modeling Procedure in the context of a Mini-Competition:
** Award in the context of a Framework Agreement
** Award in the context of a Dynamic Purchasing System

* Standard form mapping requirements:
** Communication means
** Procurement Criteria Summary
** Notice relations harmonisation

* eForm mapping requirements:
** Ensure coverage of all BTs from the new eForm Annex
** Implemented new eForm business terms
** Revision of all monetary values

* New module development: eFulfilment, eContract

* Post-Award modules alignment (eCatalogue, eOrdering, eFulfilment):
** Creation of information hubs to allow data to be provided either at document or line level if not a combination of the two
** Modelling of different charges allowing for the different requirements across the different phases
** Deliverable becomes a subclass of the Item
** PostAward Objects become Documents

* Changed rdfs:Literal data type to rdf:Plain Literal

== Change notes

== New classes

=== ePO core

* epo:AdHocChannel
* epo:AwardCriteriaSummary
* epo:AwardOutcome
* epo:Candidate
* epo:DirectContract
* epo:DynamicPurchaseSystemTechnique (renamed from epo:DynamicPurchaseSystemTechniqueUsage)
* epo:EAuctionTechnique (renamed from epo:EAuctionTechniqueUsage)
* epo:EconomicStandingSummary
* epo:ElectronicSignature
* epo:ExclusionGroundsSummary
* epo:FrameworkAgreementTechnique (renamed from epo:FrameworkAgreementTechniqueUsage)
* epo:JuryMember
* epo:MiniCompetitionAwardOutcome
* epo:NonDisclosureAgreementTerm
* epo:NonPublishedInformation
* epo:NoticeChangeInformation (renamed from epo:NoticeChange)
* epo:OfferIssuer
* epo:Offer
* epo:OriginatorRequest
* epo:ParticipationConditionsSummary
* epo:ParticipationCondition
* epo:ProcurementCriteriaSummary
* epo:ProfessionalSuitabilitySummary
* epo:QualificationCriteriaSummary
* epo:QualificationCriterion
* epo:SelectedCandidateList
* epo:SelectionCriteriaSummary
* epo:TechnicalAbilitySummary
* epo:Technique (renamed from epo:TechniqueUsage)
* epo:VehicleInformation
* adms:Identifier (renamed from epo:Identifier)

=== eCatalogue

* epo-cat:InformationHub
* epo-cat:Line
* epo-cat:PostAwardDocument
* epo-cat:Certificate (renamed from epo-cat:ItemCertificate)
* epo-cat:ItemProperty (renamed from epo-cat:ItemDescription)

=== eOrdering

* epo-ord:DeliveryAgreement
* epo-ord:AllowanceInformation (renamed from epo-ord:DiscountInformation)
* epo-ord:AllowanceChargeInformation (renamed from epo-ord:PriceModifierInformation)
* epo-ord:OrderResponseInformation
* epo-ord:OrderResponseLine
* epo-ord:OrderResponse

=== eNotice

* epo-not:PreMarketConsultationNotice

== Deleted classes

=== ePO core

* epo:ContractModification
* epo:ElementDescription
* epo:ElementModificationDescription
* epo:ElementChangeDescription
* epo:ElementConfidentialityDescription
* epo:NoticeDescription
* epo:PublicationProvision

=== eCatalogue

* epo-cat:CatalogueDocument
* epo-cat:CatalogueUpdateDocument
=== eOrdering

* epo-ful:Carrier
* epo-ful:Invoicer
* epo-ord:Beneficiary
* epo-ord:Invoicee
* epo-ord:Ordering

=== eNotice

* epo-not:PMCNotice

== New Controlled Vocabularies

=== ePO core

* at-voc:EU-programme
* at-voc:cvd-contract-type
* at-voc:green-public-procurement-criteria
* at-voc:review-body-type
* at-voc:vehicle-category

=== eCatalogue

* at-voc-new:tax-category (renamed from at-voc-new:charge-category)
* at-voc-new:tax-scheme (renamed from at-voc-new:charge-modifier)
* at-voc-new:item-classification (renamed from at-voc-new:unspc)

=== eOrdering

* at-voc-new:ResponseStatus

== Deleted Controlled Vocabularies

=== ePO core

* at-voc-new:notification-phases-content-types
* at-voc-new:legal-regime
* at-voc-new:evaluation-group-type
* at-voc:cpvsuppl

== Changed classes

[cols="1,2,2,2"]
|===
s|module|class|added attributes|deleted attributes

|ePO core|cccev:InformationConcept|dct:description|epo:hasDescription
||cccev:InformationConcept|skos:prefLabel|epo:hasName
||cccev:Requirement|dct:description|epo:hasDescription
||cccev:Requirement|skos:prefLabel|epo:hasName
||cpov:ContactPoint|dct:description|epo:hasDescription
||cpv:Person||cv:deathDate
||cpv:Person||legal:registeredAddress
||cv:Channel|dct:description|epo:hasDescription
||epo-cat:Item|epo:hasAddressURL|epo:hasURL
||epo-cat:Item||epo:hasAdditionalInformation
||epo-cat:Item||epo:hasEndpoint
||epo-cat:Item||epo:isAdhocChannel
||epo-cat:Item||epo:hasName
||epo:AgentInRole|dct:description|epo:hasDescription
||epo:AgentInRole|dct:title|epo:hasTitle
||epo:AwardCriterion|epo:hasAwardCriteriaStatedInProcurementDocuments|
||epo:AwardDecision|epo:hasAwardDecisionDate|
||epo:AwardDecision|epo:hasAdditionalNonAwardJustification|
||epo:ContractLotCompletionInformation|epo:hasPaymentValueDiscrepancyJustification|
||epo:Contract||epo:hasAccessURL
||epo:Document|dct:title|
||epo:Document|dct:issued|
||epo:Document|dct:description|
||epo:ElectronicSignature|dct:description|
||epo:Fund|dct:description|epo:hasDescription
||epo:Fund|dct:title|epo:hasTitle
||epo:GreenProcurement|epo:usesCleanVehicleDirective|
||epo:GreenProcurement||epo:hasTotalVehicles
||epo:GreenProcurement||epo:hasZeroEmissionVehicles
||epo:GreenProcurement||epo:hasCleanVehicles
||epo:LotAwardOutcome||epo:hasAwardDecisionDate
||epo:LotAwardOutcome||epo:hasAdditionalNonAwardJustification
||epo:NonDisclosureAgreementTerm|dct:description|
||epo:NonDisclosureAgreementTerm|epo:isNonDisclosureAgreementRequired|
||epo:NonPublishedInformation|epo:hasAccessibilityDate|
||epo:NonPublishedInformation|epo:hasConfidentialityJustification|
||epo:NoticeChangeInformation (renamed from epo:NoticeChange)|epo:hasAdditionalInformation|
||epo:NoticeChangeInformation (renamed from epo:NoticeChange)|epo:hasProcurementDocumentChangeDate|
||epo:NoticeChangeInformation (renamed from epo:NoticeChange)|epo:isProcurementDocumentChanged|
||epo:NoticeChangeInformation (renamed from epo:NoticeChange)|epo:hasChangeReasonDescription|
||epo:NoticeChangeInformation (renamed from epo:NoticeChange)|epo:hasChangeDescription|
||epo:Notice|epo:hasOJSIssueNumber|
||epo:Notice|epo:hasOJSType|
||epo:Notice|epo:hasLongTitle|
||epo:Notice|epo:hasNoticePublicationNumber|
||epo:Notice|epo:hasFormNumber|
||epo:Notice|epo:hasEFormsSubtype|
||epo:Notice|epo:hasAdditionalInformation|
||epo:Notice|epo:hasESenderDispatchDate|
||epo:ParticipationConditionsSummary|epo:describesObjectiveParticipationRules|
||epo:ParticipationConditionsSummary|epo:describesVerificationMethod|
||epo:ProcedureTerm||epo:hasLotAwardLimit
||epo:ProcurementCriteriaSummary|epo:indicatesPerformingStaffInformationRequirement|
||epo:ProcurementElement|dct:description|epo:hasDescription
||epo:ProcurementElement|dct:title|epo:hasTitle
||epo:ProcurementObject|epo:hasLegalBasisDescription|
||epo:ProfessionalSuitabilitySummary|epo:describesProfessionRelevantLaw|
||epo:ProfessionalSuitabilitySummary|epo:hasServiceReservedToParticularProfession|
||epo:ProfessionalSuitabilitySummary|epo:describesProfession|
||epo:PurchaseContract||epo:isWithinFrameworkAgreement
||epo:QualificationCriteriaSummary|epo:hasQualificationCondition|
||epo:QualificationCriteriaSummary|epo:hasConditionVerificationMethod|
||epo:SecurityClearanceTerm|epo:isSecurityClearanceRequired|
||epo:SecurityClearanceTerm|dct:description|epo:hasDescription
||epo:SelectionCriteriaSummary|epo:hasSelectionCriteriaStatedInProcurementDocuments|
||epo:SelectionCriteriaSummary|epo:describesMinimumLevelOfStandards|
||epo:SubcontractTerm|dct:description|epo:hasDescription
||epo:SubcontractingEstimate|dct:description|epo:hasDescription
||epo:SubmissionStatisticalInformation|epo:hasOtherCountriesReceivedTenders|
||epo:SubmissionStatisticalInformation|epo:hasNonEEAReceivedTenders|epo:hasReceivedNonEEATenders
||epo:SubmissionStatisticalInformation|epo:hasNonEUReceivedTenders|epo:hasReceivedNonEUTenders
||epo:SubmissionStatisticalInformation|epo:hasSMEReceivedTenders|epo:hasReceivedSMETenders
||epo:SubmissionTerm|epo:hasReceiptTenderDeadline|
||epo:SubmissionTerm|epo:hasReceiptPreliminaryMarketConsultationDeadline|
||epo:SubmissionTerm|epo:hasReceiptParticipationRequestDeadline|
||epo:System|dct:description|epo:hasDescription
||epo:Technique (renamed from epo:TechniqueUsage)|dct:description|epo:hasDescription
||epo:VehicleInformation|epo:hasTotalVehicles|
||epo:VehicleInformation|epo:hasZeroEmissionVehicles|
||epo:VehicleInformation|epo:hasCleanVehicles|
||foaf:Agent|dct:title|epo:hasTitle
||org:Organization|epo:hasInternetAddress|
||org:Organization|epo:hasOrganisationUnitName|epo:hasOrganisationUnit
|eCatalogue|epo-cat:Batch|epo-cat:hasManufactureDate|
||epo-cat:Brand|dct:title|epo:hasName
||epo-cat:ItemModel|dct:title|epo:hasName
||epo-cat:Item|dct:title|epo:hasName
||epo-cat:Item|dct:description|epo:hasDescription
||epo-cat:Item||epo-cat:hasExternalSpecification
||epo-cat:Item||epo-cat:hasVATRate
||epo-cat:Line|dct:description|
|eOrdering|epo-ord:DeliveryAgreement|dct:description|
||epo-ord:DeliveryInformation|epo-ord:hasDeliveryDeadline|
||epo-ord:Order|epo-ord:hasCustomerReference|
||epo-ord:Order|epo-ord:hasAccountingCost|
||epo-ord:Order|epo-ord:hasPaymentTerm|
||epo-ord:AllowanceChargeInformation (renamed from epo-ord:PriceModifierInformation)|epo-cat:hasPercentage|epo-cat:hasPricePercentage
||epo-ord:AllowanceChargeInformation (renamed from epo-ord:PriceModifierInformation)|epo-ful:hasAllowanceChargeReasonDescription|
||epo-ord:TaxInformation|epo-cat:hasPercentage|
||epo-ord:TaxInformation|dct:description|
||epo-ord:OrderResponse|epo-ord:hasResponseDescription|
|===

[cols="1,2,2,2"]
|===
s|module|class|added property|deleted property

|ePO core|cccev:InformationConcept|adms:identifier -> adms:Identifier|epo:hasID -> epo:Identifier
||cpv:Person|cv:registeredAddress|
||cv:Channel|epo:hasEndpointIdentifier -> adms:Identifier|
||dct:Location|adms:identifier -> adms:Identifier|
||epo:AdHocChannel|generalisation -> cv:Channel|
||epo:AgentInRole|epo:exposesChannel -> cv:Channel|
||epo:AwardCriteriaSummary|generalisation -> epo:ProcurementCriteriaSummary|
||epo:AwardDecision|generalisation -> epo:Document|generalisation -> epo:ProcurementElement
||epo:AwardDecision|epo:comprisesAwardOutcome -> epo:AwardOutcome|epo:comprisesLotAwardOutcome -> epo:LotAwardOutcome
||epo:AwardOutcome|epo:hasAwardedValue -> epo:MonetaryValue|
||epo:AwardOutcome|epo:hasBargainPrice -> epo:MonetaryValue|
||epo:AwardOutcome|epo:comprisesTenderAwardOutcome -> epo:TenderAwardOutcome|
||epo:AwardOutcome|epo:hasNonAwardJustification -> at-voc:non-award-justification|
||epo:AwardOutcome|epo:hasAwardStatus -> at-voc:winner-selection-status|
||epo:AwardOutcome|generalisation -> epo:ContextualProjection|
||epo:Awarder||epo:dependsOnBuyer -> epo:Buyer
||epo:BudgetProvider||epo:dependsOnBuyer -> epo:Buyer
||epo:BudgetProvider||epo:dependsOnServiceProvider -> epo:ProcurementServiceProvider
||epo:Buyer|epo:signsAwardDecision -> epo:AwardDecision|
||epo:Buyer|epo:exposesInvoiceeChannel -> cv:Channel|
||epo:Buyer|epo:indicatesInvoiceeContactPoint -> cpov:ContactPoint|
||epo:Candidate|generalisation -> epo:OfferingParty|
||epo:ConcessionEstimate|epo:hasConcessionEstimatedValue|
||epo:ContractLotCompletionInformation|epo:providesContractTotalPaymentValue -> epo:MonetaryValue|epo:hasPaymentValue -> epo:MonetaryValue
||epo:ContractLotCompletionInformation|epo:providesContractTotalPenaltyValue -> epo:MonetaryValue|epo:hasPenaltyValue -> epo:MonetaryValue
||epo:ContractTerm||epo:hasContractorLegalFormRequirement
||epo:ContractTerm|epo:hasLegalFormRequirement|epo:hasContractorLegalFormRequirementDescription
||epo:ContractTerm|epo:hasEInvoicingPermission -> at-voc:permission|
||epo:Contractor|epo:needsToBeAWinner -> epo:Winner|
||epo:Contract|generalisation -> epo:Document|generalisation -> epo:ProcurementElement
||epo:Contract|epo:specifiesDeliverable -> epo-con:Deliverable|
||epo:Contract|epo:hasContractValue -> epo:MonetaryValue|
||epo:Contract|epo:isSubjectToContractSpecificTerm -> epo:ContractSpecificTerm|
||epo:Contract|epo:isFundedBy -> epo:Fund|
||epo:ElementConfidentialityDescription|epo:hasPurpose -> epo:Purpose|
||epo:ElementConfidentialityDescription|epo-ord:hasTaxInformation -> epo-ord:TaxInformation|
||epo:DirectContract|epo:resultsFromLotAwardOutcome -> epo:LotAwardOutcome|
||epo:DirectContract|generalisation -> epo:Document|
||epo:Document|epo:hasElectronicDigest -> epo:Document|
||epo:Document|epo:hasElectronicSignature -> epo:ElectronicSignature|
||epo:EconomicStandingSummary|generalisation -> epo:SelectionCriteriaSummary|
||epo:Estimate|generalisation -> epo:ContextSpecificDescription|
||epo:ExclusionGroundsSummary|generalisation -> epo:QualificationCriteriaSummary|
||epo:ExclusionGround||epo:specifiesExclusionGround -> epo:Procedure
||epo:ExclusionGround|generalisation -> epo:QualificationCriterion|generalisation -> epo:ProcurementCriterion
||epo:FrameworkAgreementTerm||epo:hasOverallMaximumValue -> epo:MonetaryValue
||epo:FrameworkAgreementTerm|epo:hasLaunchFrameworkAgreementMaximumValue -> epo:MonetaryValue|
||epo:FrameworkAgreementTerm|epo:hasLaunchGroupFrameworkAgreementMaximumValue -> epo:MonetaryValue|
||epo:FrameworkAgreementTerm|generalisation -> epo:ContractSpecificTerm|
||epo:FrameworkAgreement|epo:resultsFromLotAwardOutcome -> epo:LotAwardOutcome|
||epo:Fund|epo:hasFundProgramme -> at-voc:EU-programme|
||epo:Fund|adms:identifier -> adms:Identifier|epo:hasID -> epo:Identifier
||epo:GreenProcurement|epo:fulfillsRequirement -> at-voc:green-public-procurement-criteria|
||epo:JuryMember|epo:playedBy -> foaf:Agent|
||epo:JuryMember|generalisation -> epo:AcquiringParty|
||epo:LotAwardOutcome||epo:comprisesTenderAwardOutcome -> epo:TenderAwardOutcome
||epo:LotAwardOutcome||epo:hasRestatedAwardedValue -> epo:MonetaryValue
||epo:LotAwardOutcome||epo:isAdoptedByBuyer -> epo:Buyer
||epo:LotAwardOutcome|epo:hasFrameworkAgreementMaximumValue -> epo:MonetaryValue|
||epo:LotAwardOutcome|epo:hasApproximateFrameworkAgreementValue -> epo:MonetaryValue|
||epo:LotAwardOutcome|generalisation -> epo:AwardOutcome|
||epo:LotGroupAwardInformation|epo:hasGroupFrameworkAgreementMaximumValue -> epo:MonetaryValue|epo:hasGroupFrameworkAgreementAwardedValue -> epo:MonetaryValue
||epo:LotGroupAwardInformation|generalisation -> epo:ContextSpecificDescription|generalisation -> epo:ContextualProjection
||epo:LotGroup||epo:hasEstimatedValue -> epo:MonetaryValue
||epo:LotGroup||epo:specifiesSelectionCriterion -> epo:SelectionCriterion
||epo:LotGroup|epo:specifiesProcurementCriterion -> epo:ProcurementCriterion|epo:specifiesAwardCriterion -> epo:AwardCriterion
||epo:LotGroup|adms:identifier -> adms:Identifier|
||epo:Lot||epo:specifiesSelectionCriterion -> epo:SelectionCriterion
||epo:Lot|epo:specifiesProcurementCriterion -> epo:ProcurementCriterion|epo:specifiesAwardCriterion -> epo:AwardCriterion
||epo:Lot||epo:hasRestatedEstimatedValue -> epo:MonetaryValue
||epo:Lot||epo:hasReservedProcurement -> at-voc:reserved-procurement
||epo:Lot||epo:hasPerformingStaffQualificationInformation -> at-voc:requirement-stage
||epo:MiniCompetitionAwardOutcome|epo:resultsFromUsingCandidateList -> epo:SelectedCandidateList|
||epo:MiniCompetitionAwardOutcome|generalisation -> epo:AwardOutcome|
||epo:MultipleStageProcedureTerm||epo:hasQualificationSystemPeriod -> epo:Period
||epo:MultipleStageProcedureTerm|generalisation -> epo:LotSpecificTerm|
||epo:MultipleStageProcedureTerm|epo:concernsNotice -> epo:Notice|
||epo:MultipleStageProcedureTerm|epo:relatesToEFormSectionIdentifier -> adms:Identifier|
||epo:MultipleStageProcedureTerm|generalisation -> epo:ContextSpecificDescription|
||epo:MultipleStageProcedureTerm|epo:hasNonPublicationJustification -> at-voc:non-publication-justification|
||epo:NoticeAwardInformation|epo:describesResultNotice -> epo-not:DirectAwardPrenotificationNotice|
||epo:NoticeAwardInformation|epo:hasApproximateFrameworkAgreementValue -> epo:MonetaryValue|
||epo:NoticeChangeInformation (renamed from epo:NoticeChange)||epo:hasElementChange -> epo:ElementChangeDescription
||epo:NoticeChangeInformation (renamed from epo:NoticeChange)|generalisation -> epo:ContextSpecificDescription|generalisation -> epo:NoticeDescription
||epo:NoticeChangeInformation (renamed from epo:NoticeChange)|epo:concernsNotice -> epo:Notice|
||epo:NoticeChangeInformation (renamed from epo:NoticeChange)|epo:relatesToEFormSectionIdentifier -> adms:Identifier|
||epo:NoticeChangeInformation (renamed from epo:NoticeChange)|epo:hasChangeJustification -> at-voc:change-corrig-justification|
||epo:Notice||epo:hasNotificationContentType -> at-voc-new:notification-phases-content-types
||epo:Notice|epo:refersToLot -> epo:Lot|
||epo:Notice|epo:conformsToSpecificLegalBasis -> at-voc:legal-basis|
||epo:OfferIssuer|epo:distributesOffer -> epo:Offer|
||epo:OfferIssuer|generalisation -> epo:OfferingParty|
||epo:OfferingParty||epo:playedByBusiness -> epo:Business
||epo:Offer|generalisation -> epo:Document|
||epo:OriginatorRequest|generalisation -> epo:Document|
||epo:ParticipationConditionsSummary|generalisation -> epo:ProcurementCriteriaSummary|
||epo:ParticipationConditionsSummary|epo:hasReservedProcurement -> at-voc:reserved-procurement|
||epo:ParticipationCondition|generalisation -> epo:ProcurementCriterion|
||epo:ParticipationCondition|epo:hasReservedProcurement -> at-voc:reserved-procurement|
||epo:ParticipationRequestProcessor||epo:dependsOnServiceProvider -> epo:ProcurementServiceProvider
||epo:ParticipationRequestProcessor||epo:dependsOnBuyer -> epo:Buyer
||epo:ParticipationRequestReceiver||epo:dependsOnServiceProvider -> epo:ProcurementServiceProvider
||epo:ParticipationRequestReceiver||epo:dependsOnBuyer -> epo:Buyer
||epo:PaymentExecutor||epo:dependsOnServiceProvider -> epo:ProcurementServiceProvider
||epo:PaymentExecutor||epo:dependsOnBuyer -> epo:Buyer
||epo:PlannedProcurementPart||epo:hasLegalBasis -> at-voc:legal-basis
||epo:PlannedProcurementPart|generalisation -> epo:ProcurementElement|generalisation -> epo:ProcurementObject
||epo:PlannedProcurementPart|epo:foreseesProcurementObject -> epo:ProcurementObject|
||epo:Procedure||epo:hasLegalBasis -> at-voc:legal-basis
||epo:Procedure||epo:hasLegalRegime -> at-voc-new:legal-regime
||epo:Procedure|epo:specifiesProcurementCriteriaSummary -> epo:ProcurementCriteriaSummary|epo:specifiesExclusionGround -> epo:ExclusionGround
||epo:ProcurementCriteriaSummary|generalisation -> cccev:Requirement|
||epo:ProcurementCriterion|epo:hasPerformingStaffQualificationInformation -> at-voc:requirement-stage|
||epo:ProcurementElement|epo:hasInternalIdentifier -> adms:Identifier|
||epo:ProcurementElement|epo:usesChannel -> cv:Channel|
||epo:ProcurementElement|epo:hasEstimatedValue -> epo:MonetaryValue|
||epo:ProcurementElement|adms:identifier -> adms:Identifier|
||epo:ProcurementObject||epo:hasID -> epo:Identifier
||epo:ProcurementObject||epo:usesChannel -> cv:Channel
||epo:ProcurementObject||epo:refersToPlannedPart -> epo:PlannedProcurementPart
||epo:ProcurementObject|epo:hasLegalBasis -> at-voc:legal-basis|
||epo:ProcurementObject|epo:foreseesConcession -> epo:ConcessionEstimate|
||epo:ProfessionalSuitabilitySummary|generalisation -> epo:SelectionCriteriaSummary|
||epo:Project|adms:identifier -> adms:Identifier|
||epo:PurchaseContract|epo:resultsFromMiniCompetitionAwardOutcome -> epo:MiniCompetitionAwardOutcome|
||epo:Purpose||epo:hasMainClassification -> at-voc:cpvsuppl
||epo:Purpose||epo:hasAdditionalClassification -> at-voc:cpvsuppl
||epo:QualificationCriteriaSummary|generalisation -> epo:ProcurementCriteriaSummary|
||epo:QualificationCriterion|generalisation -> epo:ProcurementCriterion|
||epo:ReviewDecision|epo:hasRemedyValue -> epo:MonetaryValue|
||epo:ReviewObject||epo:hasRemedyValue -> epo:MonetaryValue
||epo:ReviewObject|generalisation -> epo:Document|generalisation -> epo:ProcurementElement
||epo:ReviewProcedureInformationProvider||epo:dependsOnReviewer -> epo:Reviewer
||epo:ReviewRequest|epo:hasReviewRequestFee -> epo:MonetaryValue|epo:paidReviewRequestFee -> epo:MonetaryValue
||epo:ReviewTerm||generalisation -> epo:ProcedureSpecificTerm
||epo:Reviewer|epo:hasReviewBodyType -> at-voc:review-body-type|
||epo:SelectedCandidateList|epo:containsCandidate -> epo:Candidate|
||epo:SelectedCandidateList|epo:hasStartDate -> epo:Period|
||epo:SelectionCriteriaSummary|generalisation -> epo:QualificationCriteriaSummary|
||epo:SelectionCriterion|generalisation -> epo:QualificationCriterion|generalisation -> epo:ProcurementCriterion
||epo:SubmissionStatisticalInformation|epo:summarisesInformationForAwardOutcome -> epo:AwardOutcome|epo:summarisesInformationForLotAwardOutcome -> epo:LotAwardOutcome
||epo:SubmissionTerm|epo:hasTenderValidityPeriod -> epo:Period|epo:hasValidityPeriod -> epo:Period
||epo:TechnicalAbilitySummary|generalisation -> epo:SelectionCriteriaSummary|
||epo:TenderAwardOutcome|epo:indicatesAwardToWinner -> epo:Winner|epo:indicatesAwardOfLotToWinner -> epo:Winner
||epo:TenderAwardOutcome|epo:concernsTender -> epo:Tender|epo:describesTender -> epo:Tender
||epo:TenderProcessor||epo:dependsOnServiceProvider -> epo:ProcurementServiceProvider
||epo:TenderProcessor||epo:dependsOnBuyer -> epo:Buyer
||epo:TenderReceiver||epo:dependsOnServiceProvider -> epo:ProcurementServiceProvider
||epo:TenderReceiver||epo:dependsOnBuyer -> epo:Buyer
||epo:Tender|generalisation -> epo:Document|generalisation -> epo:ProcurementElement
||epo:Tender|epo:hasSubcontracting -> at-voc:applicability|
||epo:VehicleInformation|epo:concernsGreenProcurement -> epo:GreenProcurement|
||epo:VehicleInformation|epo:specifiesCleanVehicleDirectiveVehicleCategory -> at-voc:vehicle-category|
||epo:VehicleInformation|epo:specifiesCleanVehicleDirectiveContractType -> at-voc:cvd-contract-type|
||epo:Winner|epo:needsToBeATenderer -> epo:Tenderer|epo:dependsOnTenderer -> epo:Tenderer
||foaf:Agent|adms:identifier -> adms:Identifier|epo:hasID -> epo:Identifier
||foaf:Person|epo:hasCertification -> epo-cat:Certificate|
||locn:Address|adms:identifier -> adms:Identifier|epo:hasID -> epo:Identifier
||org:Organization|epo:hasLegalIdentifier -> adms:Identifier|
||org:Organization|epo:hasRegistrationCountry -> at-voc:country|
||org:Organization|epo:hasCertification -> epo-cat:Certificate|
||org:Organization|epo:hasTaxIdentifier -> adms:Identifier|
|eCatalogue|epo-cat:CatalogueLine|generalisation -> epo-cat:Line|
||epo-cat:CatalogueLine||epo:hasID -> epo:Identifier
||epo-cat:CatalogueLine||epo-cat:specifiesItem -> epo-cat:Item
||epo-cat:Catalogue||epo:hasValidityPeriod -> epo:Period
||epo-cat:Catalogue|generalisation -> epo-cat:PostAwardDocument|
||epo-cat:Catalogue|epo:specifiesCatalogueReceiver -> epo:CatalogueReceiver|epo-cat:isReceivedByCatalogueReceiver -> epo:CatalogueReceiver
||epo-cat:Catalogue|epo:specifiesCatalogueProvider -> epo:CatalogueProvider|epo-cat:isReceivedByCatalogueProvider -> epo:CatalogueProvider
||epo-cat:Catalogue|epo:specifiesBuyer -> epo:Buyer|epo:isIntendedForBuyer -> epo:Buyer
||epo-cat:ChargeInformation|generalisation -> epo-ord:AllowanceChargeInformation|generalisation -> epo-ord:PriceModifierInformation
||epo-cat:ChargeInformation||epo-cat:hasChargeCategory -> at-voc-new:charge-category
||epo-cat:ChargeInformation||epo-cat:hasChargeCategoryModifier -> at-voc-new:charge-modifier
||epo-cat:InformationHub|epo-cat:isSpecificToLine -> epo-cat:Line|
||epo-cat:InformationHub|generalisation -> epo:ContextSpecificDescription|
||epo-cat:ItemProperty (renamed from epo-cat:ItemDescription)||generalisation -> epo:ElementDescription
||epo-cat:Item|epo-ord:hasTaxInformation -> epo-ord:TaxInformation|
||epo-cat:Item|epo:hasCertification -> epo-cat:Certificate|epo-cat:hasCertification -> epo-cat:ItemCertificate
||epo-cat:Item|epo:hasSellerItemID -> adms:Identifier|epo:hasCertification -> epo-cat:ItemCertificate
||epo-cat:Item|dct:isReplacedBy -> epo-cat:Item|dct:isReplaceBy -> epo-cat:Item
||epo-cat:Item|epo:hasSerialID -> adms:Identifier|
||epo-cat:Item|epo-cat:hasExternalSpecification -> epo:Document|
||epo-cat:Line|epo-cat:specifiesItem -> epo-cat:Item|
||epo-cat:Line|adms:identifier -> adms:Identifier|
||epo-cat:PostAwardDocument|generalisation -> epo:Document|
||epo-cat:PostAwardDocument|epo-cat:hasDocumentType -> at-voc-new:document-type|
||epo-cat:PostAwardDocument|epo:hasDocumentStatus -> at-voc-new:document-status|
||epo-cat:Price|epo-ord:hasPriceDiscountInformation -> epo-ord:AllowanceInformation|
||epo-cat:Price|epo:hasPriceSurchargeInformation -> epo-cat:ChargeInformation|
||epo-cat:ProductSpecification|generalisation -> epo-cat:PostAwardDocument|generalisation -> epo:Document
|eOrdering|epo-ord:ContractInformation|generalisation -> epo-cat:InformationHub|generalisation -> epo:ContextSpecificDescription
||epo-ord:DeliveryAgreement|epo-ord:specifiesDeliveryAgreementLocation -> dct:Location|
||epo-ord:DeliveryInformation||epo:concernsBeneficiary -> epo-ord:Beneficiary
||epo-ord:DeliveryInformation|epo-ord:specifiesPlaceOfDelivery -> dct:Location|epo-ord:concernsPlaceOfDelivery -> dct:Location
||epo-ord:DeliveryInformation||epo-ord:concernsPlaceOfStorage
||epo-ord:DeliveryInformation|epo-ord:specifiesGeneralDeliveryAgreement -> epo-ord:DeliveryAgreement|
||epo-ord:DeliveryInformation|epo-ord:specifiesSpecificDeliveryAgreement -> epo-ord:DeliveryAgreement|
||epo-ord:DeliveryInformation|epo-ful:hasTrackingID -> adms:Identifier|
||epo-ord:OrderLine||epo-cat:specifiesItem -> epo-cat:Item
||epo-ord:OrderLine|epo-cat:hasQuantity -> epo:Quantity|epo-cat:hasOrderQuantity -> epo:Quantity
||epo-ord:OrderLine|generalisation -> epo-cat:Line|
||epo-ord:Order||epo:hasValidityPeriod -> epo:Period
||epo-ord:Order||epo-ord:invoicedToInvoicee -> epo-ord:Invoicee
||epo-ord:Order||epo-ord:supersedesOrder -> epo-ord:Order
||epo-ord:Order|epo-ord:hasTotalTaxInclusiveAmount -> epo:MonetaryValue|
||epo-ord:Order|epo-ord:hasTotalTaxExclusiveAmount -> epo:MonetaryValue|
||epo-ord:Order|epo:specifiesDespatcher -> epo-ful:Despatcher|
||epo-ord:Order|epo-ord:hasTotalLineAmount -> epo:MonetaryValue|
||epo-ord:Order|epo:refersToProject -> epo:Project|
||epo-ord:Order|generalisation -> epo-cat:PostAwardDocument|
||epo-ord:Order|epo-ord:hasTotalAllowanceAmount -> epo:MonetaryValue|
||epo-ord:Order|epo:specifiesSeller -> epo-ord:Seller|epo-ord:isSubmittedToSeller -> epo-ord:Selle
||epo-ord:Order|epo-ord:hasRoundingAmount -> epo:MonetaryValue|
||epo-ord:Order|epo-ord:specifiesAllowanceInformation -> epo-ord:AllowanceInformation|epo-ord:specifiesDiscountInformation -> epo-ord:DiscountInformatio
||epo-ord:Order|epo-ord:hasPrepaidAmount -> epo:MonetaryValue|
||epo-ord:Order|epo-ord:hasAmountDueForPayment -> epo:MonetaryValue|
||epo-ord:Order|epo:specifiesBuyer -> epo:Buyer|epo-ord:isSubmittedByBuyer -> epo:Buyer
||epo-ord:Order|epo-ord:hasTotalChargeAmount -> epo:MonetaryValue|
||epo-ord:OriginatorInformation|epo-ord:concernsOriginatorRequest -> epo:OriginatorRequest|
||epo-ord:OriginatorInformation|generalisation -> epo-cat:InformationHub|generalisation -> epo:ContextSpecificDescription
||epo-ord:AllowanceChargeInformation (renamed from epo-ord:PriceModifierInformation)|generalisation -> epo-cat:InformationHub|generalisation -> epo:ContextSpecificDescription
||epo-ord:AllowanceChargeInformation (renamed from epo-ord:PriceModifierInformation)|epo:isCalculatedOn -> epo:MonetaryValue|
||epo-ord:AllowanceChargeInformation (renamed from epo-ord:PriceModifierInformation)|epo-ord:hasTaxInformation -> epo-ord:TaxInformation|
||epo-ord:AllowanceChargeInformation (renamed from epo-ord:PriceModifierInformation)|epo-cat:hasAmount -> epo:MonetaryValue|epo-cat:hasFixedAmount -> epo:MonetaryValue
||epo-ord:AllowanceChargeInformation (renamed from epo-ord:PriceModifierInformation)|epo-ful:hasAllowanceChargeReason -> at-voc-new:allowance-charge-reason|
||epo-ord:TaxInformation|epo:isCalculatedOn -> epo:MonetaryValue|
||epo-ord:TaxInformation|epo-cat:hasAmount -> epo:MonetaryValue|
||epo-ord:TaxInformation|generalisation -> epo-cat:InformationHub|
||epo-ord:TaxInformation|epo-cat:hasTaxCategory -> at-voc-new:tax-category|
||epo-ord:TaxInformation|epo-cat:hasTaxScheme -> at-voc-new:tax-scheme|
||epo-ord:TaxInformation|epo-cat:hasVATCategory -> at-voc-new:vat-category|
||epo-ord:OrderResponseInformation|generalisation -> epo-cat:InformationHub|
||epo-ord:OrderResponseInformation|epo-ord:isSpecificToOrderResponseLine -> epo-ord:OrderResponseLine|
||epo-ord:OrderResponseInformation|epo-ord:hasDeliveryPeriod -> epo:Period|
||epo-ord:OrderResponseInformation|epo-ord:hasAcceptanceStatus -> at-voc-new:ResponseStatus|
||epo-ord:OrderResponseLine|epo-ord:isSubmittedForOrderLine -> epo-ord:OrderLine|
||epo-ord:OrderResponseLine|generalisation -> epo-ord:OrderLine|
||epo-ord:OrderResponse|epo-ord:comprisesOrderResponseLine -> epo-ord:OrderResponseLine|
||epo-ord:OrderResponse|epo-ord:isSubmittedForOrder -> epo-ord:Order|
||epo-ord:OrderResponse|epo-ord:specifiesOrderResponseInformation -> epo-ord:OrderResponseInformation|
||epo-ord:OrderResponse|epo-ord:specifiesSeller -> epo-ord:Seller|
||epo-ord:OrderResponse|epo-ord:specifiesBuyer -> epo:Buyer|
||epo-ord:OrderResponse|epo-ord:implementsContract -> epo:Contract|
|eNotice|epo-not:CompetitionNotice|epo:announcesLot -> epo:Lot|epo-not:announcesLot -> epo:Lot
||epo-not:CompetitionNotice|epo:announcesLotGroup -> epo:LotGroup|epo-not:announcesLotGroup -> epo:LotGroup
||epo-not:CompetitionNotice|epo:announcesRole -> epo:AgentInRole|epo-not:announcesRole -> epo:AgentInRole
||epo-not:CompetitionNotice|epo:announcesProcedure -> epo:Procedure|epo-not:announcesProcedure -> epo:Procedure
||epo-not:CompletionNotice|epo:announcesCompletionOfContract -> epo:Contract|
||epo-not:CompletionNotice|epo:refersToAwardDecision -> epo:AwardDecision|
||epo-not:CompletionNotice|epo:refersToLot -> epo:Lot|
||epo-not:CompletionNotice|epo:announcesReviewObject -> epo:ReviewObject|
||epo-not:CompletionNotice|epo:refersToLotGroupAwardInformation -> epo:LotGroupAwardInformation|
||epo-not:CompletionNotice|epo:refersToRole -> epo:AgentInRole|
||epo-not:CompletionNotice|epo:refersToNoticeAwardInformation -> epo:NoticeAwardInformation|
||epo-not:CompletionNotice|epo:announcesRole -> epo:AgentInRole|
||epo-not:CompletionNotice|epo:refersToLotGroup -> epo:LotGroup|
||epo-not:CompletionNotice|epo:refersToProcedure -> epo:Procedure|
||epo-not:ContractModificationNotice|epo:refersToLotGroup -> epo:LotGroup|
||epo-not:ContractModificationNotice|epo:refersToContractToBeModified -> epo:Contract|epo-not:refersToContractToBeModified -> epo:Contract
||epo-not:ContractModificationNotice|epo:refersToLot -> epo:Lot|
||epo-not:ContractModificationNotice|epo:announcesRole -> epo:AgentInRole|
||epo-not:ContractModificationNotice|epo:refersToNoticeAwardInformation -> epo:NoticeAwardInformation|
||epo-not:ContractModificationNotice|epo:refersToAwardDecision -> epo:AwardDecision|
||epo-not:ContractModificationNotice|epo:refersToProcedure -> epo:Procedure|
||epo-not:ContractModificationNotice|epo:refersToLotGroupAwardInformation -> epo:LotGroupAwardInformation|
||epo-not:ContractModificationNotice|epo:announcesContractAmendment -> epo-con:ContractAmendment|
||epo-not:DirectAwardPrenotificationNotice|epo:announcesLotGroupAwardInformation -> epo:LotGroupAwardInformation|
||epo-not:DirectAwardPrenotificationNotice|epo:announcesContract -> epo:Contract|
||epo-not:DirectAwardPrenotificationNotice|epo:announcesLot -> epo:Lot|
||epo-not:DirectAwardPrenotificationNotice|epo:announcesRole -> epo:AgentInRole|
||epo-not:DirectAwardPrenotificationNotice|epo:announcesNoticeAwardInformation -> epo:NoticeAwardInformation|
||epo-not:DirectAwardPrenotificationNotice|epo:announcesProcedure -> epo:Procedure|epo-not:announcesProcedure -> epo:Procedure
||epo-not:DirectAwardPrenotificationNotice|epo:announcesLotGroup -> epo:LotGroup|
||epo-not:DirectAwardPrenotificationNotice|epo:announcesAwardDecision -> epo:AwardDecision|
||epo-not:PlanningNotice|epo:announcesPlannedProcurementPart -> epo:PlannedProcurementPart|epo-not:announcesPlannedProcurementPart -> epo:PlannedProcurementPart
||epo-not:PlanningNotice|epo:announcesRole -> epo:AgentInRole|
||epo-not:PreMarketConsultationNotice|generalisation -> epo:Notice|
|===

include::partial$feedback.adoc[]