== *eProcurement Ontology 3.0.1*

The release of version 3.0.1 and its corresponding technical files can be found link:https://github.com/OP-TED/ePO/tree/v3.0.1[here].

RDF representation of the eProcurement ontology can be downloaded link:https://github.com/OP-TED/ePO/tree/v3.0.1/implementation/ePO/owl_ontology[here].

RDF representation of the eCatalogue module can be downloaded link:https://github.com/OP-TED/ePO/tree/v3.0.1/implementation/eCatalogue/owl_ontology[here].

RDF representation of the eNotice module can be downloaded link:https://github.com/OP-TED/ePO/tree/v3.0.1/implementation/eNotice/owl_ontology[here].


== Release notes

This release was meant to clean up the model.

=== General changes

|===
|*Metadata*|*Value*

|Reference ePO version|3.0.0
|Target ePO version|3.0.1
|Authors|Andreea Pasăre, Eugeniu Costetchi
|Date|2022-09-23
|===

* All subclasses of epo:Notice have been moved to a separate module, eNotice.
* The prefix used for the eNotice module is _“epo-not:”_.
* The prefix used for the eCatalogue module is _“epo-cat”_.
* Diagrams were cleaned up to provide a better user readability.

=== New classes

* epo:ConcessionEstimate
* epo:IndefiniteDuration
* epo:SpecificDuration

=== Changed classes

==== Procurement object package

|===
|*class*|*added attributes*|*deleted attributes*

|epo:Procedure||epo:hasLotMinimumSubmission
|epo:Procedure||epo:hasLotSubmissionLimit
|epo:Procedure||epo:hasMaximumNumberOfLotsToBeAwarded
|epo:Tender||epo:hasCalculationMethod
|===

|===
|*class*|*added property*|*deleted property*

|epo:Lot|time:unitType -> time:TemporalUnit|
|epo:Lot|epo:hasRestatedEstimatedValue -> epo:MonetaryValue|
|epo:Tender|epo:foreseesContractSpecificTerm -> epo:ContractSpecificTerm|
|epo:Tender|epo:foreseesConcession -> epo:ConcessionEstimate|
|epo:Tender||epo:hasEstimatedUserConcessionRevenue -> epo:MonetaryValue
|===

==== Agent package

|===
|*class*|*added attributes*|*deleted attributes*

|org:Organization|epo:hasBuyerLegalTypeDescription|epo:hasBuyerTypeDescription
|org:Organization|epo:hasMainActivityDescription|
|===

|===
|*class*|*added property*|*deleted property*

|org:Organization|added property (outgoing connector)|deleted property (outgoing connector)
|org:Organization|epo:hasMainActivity -> at-voc:main-activity|epo:hasMainActivityType -> at-voc:main-activity
|===

==== Role package

|===
|*class*|*added attributes*|*deleted attributes*

|epo:Buyer||epo:hasBuyerTypeDescription
|===

|===
|*class*|*added property*|*deleted property*

|epo:BuyerSignatorySide||epo:hasEstimatedBuyerConcessionRevenue -> epo:MonetaryValue
|epo:Buyer|epo:dependsOnBuyer -> epo:Awarder|epo:dependsOnBuyer -> epo:Buyer
|===

==== Term package

|===
|*class*|*added attributes*|*deleted attributes*

|epo:MultipleStageProcedureTerm|epo:hasQualificationSystemRenewalDescription|
|epo:ProcedureTerm|epo:hasLotAwardCombination|
|epo:ProcedureTerm|epo:hasMaximumLotSubmissionAllowed|epo:hasLotSubmissionLimit
|epo:ProcedureTerm|epo:hasMaximumNumberOfLotsToBeAwarded|
|epo:ProcedureTerm|epo:hasNationalProcedureRules|
|epo:ProcedureTerm|epo:isOneLotOnlyAllowed|
|epo:ProcedureTerm|epo:isSubmissionForAllLotsAllowed|
|epo:SubmissionTerm|epo:hasReceiptExpressionDeadline (from epo:ProcedureTerm)|
|===

|===
|*class*|*added property*|*deleted property*

|epo:ContractTerm|epo:definesContractDuration -> epo:Duration|
|epo:MultipleStageProcedureTerm|epo:definesContractPeriod -> epo:Period|
|epo:MultipleStageProcedureTerm|epo:hasQualificationSystemPeriod -> epo:Period|
|epo:ProcedureTerm|epo:hasQualificationSystemDuration -> epo:Duration|
|epo:SubmissionTerm|generalisation -> epo:ProcedureSpecificTerm|
|===

==== Contextual description package

|===
|*class*|*added attributes*|*deleted attributes*

|epo:LotAwardOutcome|epo:hasNonAwardedContractNumber|
|epo:LotAwardOutcome|epo:hasNonAwardedContractTitle|
|epo:ConcessionEstimate|epo:hasCalculationMethod (from epo:Tender)|
|===

|===
|*class*|*added property*|*deleted property*

|epo:LotAwardOutcome|epo:hasBuyerLegalType -> at-voc:buyer-legal-type|epo:hasLegalType -> at-voc:buyer-legal-type
|epo:ConcessionEstimate|epo:hasEstimatedUserConcessionRevenue -> epo:MonetaryValue (from epo:Tender)|
|epo:ConcessionEstimate|epo:hasEstimatedBuyerConcessionRevenue -> epo:MonetaryValue (from epo:Tender)|
|===

==== Document package

|===
|*class*|*added property*|*deleted property*

|epo:Document|generalisation -> epo:Estimate|
|epo:Document|epo:isBasedOnImplementingRegulation -> at-voc:legal-basis|epo:hasImplementingRegulation -> at-voc:implementation-regulation
|===

==== Empirical types package

|===
|*class*|*added attributes*|*deleted attributes*

|epo:Duration||time:numericDuration
|epo:SpecificDuration|time:numericDuration|
|===

|===
|*class*|*added property*|*deleted property*

|epo:Duration|epo:refersToProcedure -> epo:Procedure (from epo:ResultNotice)|
|epo:IndefiniteDuration||time:unitType -> time:TemporalUnit
|epo:SpecificDuration|generalisation -> epo:Duration|
|epo:SpecificDuration|generalisation -> epo:Duration|
|===

==== eCatalogue module

|===
|*class*|*added attributes*|*deleted attributes*

|epo-cat:ChargeInformation||epo-cat:hasPricePercentage
|===

|===
|*class*|*added property*|*deleted property*

|epo-cat:Catalogue|comprisesCatalogueLine -> epo-cat:CatalogueLine|
|epo-cat:ChargeInformation|epo-cat:isSubordinatedToContract -> epo:Contract|epo-cat:isSubordinatedTo -> epo:Contract
|epo-cat:ChargeInformation||epo-cat:hasFixedAmount -> epo:MonetaryValue
|===

==== eNotice module

|===
|*class*|*added property*|*deleted property*

|epo-not:CompetitionNotice (from epo:CompetitionNotice)|epo-not:announcesLot -> epo:Lot|epo:announcesLot -> epo:Lot
|epo-not:CompetitionNotice (from epo:CompetitionNotice)|epo-not:announcesLotGroup -> epo:LotGroup|epo:announcesLotGroup -> epo:LotGroup
|epo-not:CompetitionNotice (from epo:CompetitionNotice)|epo-not:announcesRole -> epo:AgentInRole|epo:announcesRole -> epo:AgentInRole
|epo-not:CompetitionNotice (from epo:CompetitionNotice)|epo-not:announcesProcedure -> epo:Procedure|epo:announcesProcedure -> epo:Procedure
|epo-not:ContractModificationNotice (from epo:ContractModificationNotice)|epo-not:refersToContractToBeModified -> epo:Contract|epo:refersToContractToBeModified -> epo:Contract
|epo-not:DirectAwardPrenotificationNotice (from epo:DirectAwardPrenotificationNotice)|epo-not:announcesProcedure -> epo:Procedure|epo:announcesProcedure -> epo:Procedure
|epo-not:PlanningNotice (from epo:PlanningNotice)|epo-not:announcesPlannedProcurementPart -> epo:PlannedProcurementPart|epo:announcesPlannedProcurementPart -> epo:PlannedProcurementPart
|epo-not:ResultNotice|epo-not:announcesNonPublishedElement -> epo:PublicationProvision|epo:announcesNonPublishedElement -> epo:PublicationProvision
|epo-not:ResultNotice|epo-not:refersToRole -> epo:AgentInRole|epo:refersToRole -> epo:AgentInRole
|epo-not:ResultNotice|epo-not:announcesLotAwardOutcome -> epo:LotAwardOutcome|epo:announcesLotAwardOutcome -> epo:LotAwardOutcome
|epo-not:ResultNotice|epo-not:refersToProcedureTerm -> epo:ProcedureTerm|epo:refersToProcedureTerm -> epo:ProcedureTerm
|epo-not:ResultNotice|epo-not:refersToLot -> epo:Lot|epo:refersToLot -> epo:Lot
|epo-not:ResultNotice|epo-not:announcesRole -> epo:AgentInRole|epo:announcesRole -> epo:AgentInRole
|epo-not:ResultNotice|epo-not:refersToReviewTerm -> epo:ReviewTerm|epo:refersToReviewTerm -> epo:ReviewTerm
|epo-not:ResultNotice|epo-not:announcesTender -> epo:Tender|epo:announcesTender -> epo:Tender
|epo-not:ResultNotice|epo-not:refersToLotGroup -> epo:LotGroup|epo:refersToLotGroup -> epo:LotGroup
|epo-not:ResultNotice|epo-not:announcesContract -> epo:Contract|epo:announcesContract -> epo:Contract
|epo-not:ResultNotice|epo-not:announcesNoticeAwardInformation -> epo:NoticeAwardInformation|epo-not:announcesNoticeAwardInformation -> epo:NoticeAwardInformation
|epo-not:ResultNotice|epo-not:announcesLotGroupAwardInformation -> epo:LotGroupAwardInformation|epo:announcesLotGroupAwardInformation -> epo:LotGroupAwardInformation
|===

== *ePO - eProcurement Ontology 3.0.0*

The ultimate objective of the e-procurement ontology (ePO) is to put forth a commonly agreed OWL ontology that will conceptualise, formally encode and make available in an open, structured and machine-readable format data about public procurement, covering it from end to end, i.e. from notification, through tendering to awarding, ordering, invoicing and payment. It is the intention of the e-procurement ontology to unify existing practices, thus facilitating seamless exchange, access and reuse of data.

In the framework of this project, we will identify and give examples of each step of the process for creating the e-procurement ontology. Clearly specifying the roles of the different actors and the input required of them within the timeline of creating the ontology. The different phases needed to create the ontology and the intermediary processes within these phases will be clearly defined giving examples taken from the 3 use cases. In parallel to this process, a working group composed of stakeholders from multiple interested groups will be set up. This working group will decide by consensus on how the ontology should be developed at all stages and may decide to adopt the first draft of the specification proposed and described during the first meeting. This project will provide the working group with the process, methodology and technology to be followed for developing the final version of the e-procurement ontology.

The release of version 3.0.0 and its corresponding technical files can be found link:https://github.com/OP-TED/ePO/tree/v3.0.0[here].

RDF representation of the eProcurement ontology can be downloaded link:https://github.com/OP-TED/ePO/tree/v3.0.0/analysis_and_design/transformation_output/ePO/owl_ontology[here].

== Release notes

=== General changes

|===
|*Metadata*|*Value*

|Reference ePO version|3.0.0 beta
|Target ePO version|3.0.0
|Authors|Andreea Pasăre, Eugeniu Costetchi
|Date|2022-07-28
|===

* Attributes were consistently added with the “_has_”/“_is_” prefix in order to conform to the convention that attribute and relation names must start with a lowercase letter. Previously all attributes started with the capital letter.
* Attribute types were migrated from _UML_ and _epo_ datatypes into XSD/RDFS datatypes. The inventory of used data types is provided in the _datatype_ package of the model.
* Packages have been reorganised as presented below.
* New modules (as EA _root nodes_) have been created (organisation and inventory to be provided elsewhere). Some classes from the _epo_ module were moved into other modules for future modelling, as may be mentioned in this document as deleted.
* The main requirements considered in this refactoring exercise was conformance to a) the TED https://simap.ted.europa.eu/web/simap/eforms[eForms] as specified in the regulation Annexe and b) the TED https://simap.ted.europa.eu/web/simap/standard-forms-for-public-procurement[Standard Forms].
* The conceptual guidelines considered in this refactoring were a) pinning of the concepts under an upper level ontology, while taking into consideration b) multi phase life cycle of the procurement process. This will be detailed elsewhere.

=== New classes

* epo:ProcurementProcessInformation
* cccev:Evidence
* cccev:InformationConcept

=== Deleted classes

* epo:CompetitionTerminationInformation
* epo:RecurrenceInformation

=== New Controlled Vocabularies

* at-voc:confidentiality-level

=== Changed classes

=== Procurement object package

|===
|*class*|*added attributes*|*deleted attributes*

|epo:Lot|epo:hasRecurrenceDescription|
|epo:Lot|epo:isRecurrent|
|epo:Procedure|epo:hasAdditionalInformation|
|epo:Procedure|epo:hasRecurrenceDescription|
|epo:Procedure|epo:isCoveredByGPA|
|epo:Procedure|epo:isJointProcurement|
|epo:Procedure|epo:isRecurrent|
|epo:Tender|epo:isVariant|epo:hasVariant
|===

|===
|*class*|*added property*|*deleted property*

|epo:Lot|epo:foreseesContractSpecificTerm -> epo:ContractSpecificTerm|epo:foreseesContractTerm -> epo:ContractSpecificTerm
|epo:PlannedProcurementPart|epo:foreseesTechnique -> epo:TechniqueUsage|
|epo:Procedure|epo:usesTechnique -> epo:TechniqueUsage|
|epo:Procedure|epo:isResponsabilityOfBuyer -> epo:Buyer|
|===

=== Agent package


|===
|*class*|*added attributes*|*deleted attributes*

|cpv:Person|person:birthName|epo:hasBirthFamilyName
|cpv:Person|cv:birthDate|epo:hasDateOfBirth
|cpv:Person|cv:deathDate|epo:hasDateOfDeath
|===

|===
|*class*|*added property*|*deleted property*

|cpv:Person|legal:registeredAddress -> locn:Address|epo:hasRegisteredAddress -> locn:Address
|org:OrganisationGroup|generalisation -> org:Organization|
|org:Organization|epo:hasMainActivityType -> at-voc:main-activity|
|org:Organization|legal:registeredAddress -> locn:Address|epo:hasRegisteredAddress -> locn:Address
|org:Organization|cv:address -> locn:Address|epo:hasAddress -> locn:Address
|org:Organization|epo:hasBuyerType -> at-voc:buyer-legal-type|
|org:Organization|epo:hasLegalType -> at-voc:buyer-legal-type|epo:hasBuyerType -> at-voc:buyer-legal-type
|===

=== Role package


|===
|*class*|*added attributes*|*deleted attributes*

|epo:Buyer||epo:isResponsibleForProcedure
|===


|===
|*class*|*added property*|*deleted property*

|epo:Buyer||epo:hasMainActivityType -> at-voc:main-activity
|epo:Buyer||epo:hasBuyerType -> at-voc:buyer-legal-type
|===

=== Location package

|===
|*class*|*added attributes*|*deleted attributes*

|cpov:ContactPoint|cpov:email|cpov:hasEmail
|cpov:ContactPoint|cpov:telephone|cpov:hasTelephone
|locn:Address|locn:adminUnitL1|
|locn:Address|locn:adminUnitL2|
|locn:Geometry:Class|cv:coordinates|locn:coordinates
|locn:Geometry:Class|cv:latitude|locn:latitude
|locn:Geometry:Class|locn:longitude|cv:longitude
|===

|===
|*class*|*added property*|*deleted property*

|cpov:ContactPoint|cv:address -> locn:Address|epo:hasAddress -> locn:Address
|locn:Address|epo:hasNutsCode -> at-voc:nuts|locn:adminUnitL2 -> at-voc:nuts
|locn:Address|epo:hasCountryCode -> at-voc:country|locn:adminUnitL1 -> at-voc:country
|===

=== Term package

|===
|*class*|*added attributes*|*deleted attributes*

|epo:FrameworkAgreementTerm||epo:hasBuyerCoverage
|epo:FrameworkAgreementTerm|hasBuyerCategoryDescription|renamed from epo:hasFrameworkBuyerCategory
|epo:FrameworkAgreementTerm||epo:hasMaximumNumberOfAwardedTenderers
|epo:FrameworkAgreementTerm|epo:hasMaximumParticipantsNumber|
|epo:ProcedureTerm|epo:hasCrossBorderLaw|
|epo:ProcedureTerm|epo:isAwardedByCPB|
|epo:SubmissionTerm|epo:hasEAuctionURL|
|===

|===
|*class*|*added property*|*deleted property*

|epo:ReviewTerm|generalisation -> epo:ProcedureSpecificTerm|
|===
=== Criterion package


|===
|*class*|*added attributes*|*deleted attributes*

|cccev:InformationConcept|epo:hasDescription|
|cccev:InformationConcept|epo:hasName|
|===

|===
|*class*|*added property*|*deleted property*

|cccev:Constraint|cccev:constrains -> cccev:InformationConcept|
|cccev:Evidence|cccev:supportsRequirement -> cccev:Requirement|
|cccev:Evidence|cccev:supportsConcept -> cccev:InformationConcept|
|cccev:Evidence|cccev:confidentialityLevelType -> at-voc:confidentiality-level|
|cccev:InformationConcept|epo:hasID -> epo:Identifier|
|===

=== Technique package


|===
|*class*|*added attributes*|*deleted attributes*

|epo:DynamicPurchaseSystemTechniqueUsage (renamed from epo:DynamicPurchaseSystemTechnique)||epo:hasDPSTermination
|epo:EAuctionTechniqueUsage (renamed from epo:EAuctionTechnique)||epo:hasEAuctionURL
|epo:FrameworkAgreementTechniqueUsage (renamed from epo:FrameworkAgreementTechnique)||epo:hasFrameworkBuyerCategory
|epo:FrameworkAgreementTechniqueUsage (renamed from epo:FrameworkAgreementTechnique)||epo:hasFrameworkDurationJustification
|epo:FrameworkAgreementTechniqueUsage (renamed from epo:FrameworkAgreementTechnique)||epo:hasMaximumParticipantsNumber
|===


|===
|*class*|*added property*|*deleted property*

|epo:EAuctionTechniqueUsage (renamed from epo:EAuctionTechnique)||epo:hasEAuctionUsage -> at-voc:usage
|epo:TechniqueUsage (renamed from epo:Technique)|epo:hasUsage -> at-voc:usage|renamed from epo:hasEAuctionUsage -> at-voc:usage
|===

=== Contextual description package

|===
|*class*|*added attributes*|*deleted attributes*

|epo:SubmissionStatisticalInformation|epo:hasEUReceivedTenders|
|epo:SubmissionStatisticalInformation|epo:hasReceivedNonEUTenders|
|epo:ProcurementProcessInformation|epo:isCompetitionTerminated|
|epo:ProcurementProcessInformation|epo:isDPSTerminated|
|epo:ProcurementProcessInformation|epo:isToBeRelaunched|
|===

|===
|*class*|*added property*|*deleted property*

|epo:NoticeAwardInformation|epo:hasMaximumFrameworkAgreementAwardedValue -> epo:MonetaryValue|epo:hasTotalFrameworkAgreementAwardedValue -> epo:MonetaryValue
|epo:NoticeAwardInformation|epo:hasProcurementHighestReceivedTenderValue -> epo:MonetaryValue|
|epo:NoticeAwardInformation|epo:hasProcurementLowestReceivedTenderValue -> epo:MonetaryValue|
|epo:NoticeAwardInformation|epo:hasTotalAwardedValue -> epo:MonetaryValue|epo:hasTotalContractAwardedValue -> epo:MonetaryValue
|epo:ProcurementProcessInformation|generalisation -> epo:ProcurementProcessInformation|
|epo:ProcurementProcessInformation|epo:concernsLot -> epo:Lot|epo:concernsLotRelaunch -> epo:Lot (epo:RelaunchInformation as target class)
|epo:ProcurementProcessInformation|epo:concernsProcedure -> epo:Procedure|epo:concernsProcedureRelaunch -> epo:Procedure (epo:RelaunchInformation as target class)
|epo:ProcurementProcessInformation|epo:concernsPreviousNotice -> epo:Notice|
|===

=== Document package

|===
|*class*|*added property*|*deleted property*

|epo:ResultNotice|epo:refersToRole -> epo:AgentInRole|
|===


== Pre-release ePO 3.0.0 beta

|===
|*Metadata*|*Value*

|Reference ePO version|3.0.0 alpha
|Target ePO version|3.0.0 beta
|Authors|Andreea Pasăre, Eugeniu Costetchi
|Date|2022-06-04
|===
=== New classes

* epo:ConcessionContract
* foaf:Person
* epo:ContractSpecificTerm
* epo:ProcessPlanningTerm
* cccev:Constraint
* cccev:Criterion
* cccev:Requirement
* epo:Recurrence Information
* epo:CompetitionTerminationInformation
* epo:ContextSpecificDescription
* epo:ContextualProjection
* epo:Estimate
* epo:StatisticalInformation

=== Changed classes

==== Procurement object package

|===
|*class*|*added attributes*|*deleted attributes*

|epo:Lot|epo:isCoveredbyGPA|epo:hasGPAUsage
|epo:Lot|epo:isUsingEUFunds|epo:hasEstimatedTenderInvitationDate
|epo:Lot|epo:isSMESuitable|epo:hasAwardDateScheduled
|epo:Lot|epo:hasAdditionalInformation|
|epo:PlannedProcurementPart|epo:isUsingEUFunds|
|epo:PlannedProcurementPart|epo:isSMESuitable|
|epo:PlannedProcurementPart|epo:hasAdditionalInformation|
|epo:PlannedProcurementPart||epo:hasEstimatedContractNoticePublicationDate
|epo:Procedure||epo:isCompetitionTermination
|epo:Purpose||epo:hasRecurrenceDescription
|epo:Purpose||epo:hasRecurrence
|epo:Purpose||epo:hasOptionsDescription
|epo:Purpose||epo:hasOptions
|epo:Contract||epo:hasWinnerDecisionDate
|epo:Contract|epo:hasAccessURL|epo:hasAccessAddress
|epo:ReviewDecision (renamed from epo:ReviewDecisionInformation)|epo:hasDecisionDate|
|epo:ReviewObject (renamed from epo:ReviewInformation)|epo:hasElementReference|
|epo:ReviewObject (renamed from epo:ReviewInformation)||epo:hasReviewTitle
|epo:ReviewObject (renamed from epo:ReviewInformation)||epo:hasReviewDescription
|epo:ReviewObject (renamed from epo:ReviewInformation)||epo:hasReviewDate
|epo:ReviewRequest (renamed from epo:ReviewRequestInformation)|epo:hasRequestDate|
|===

|===
|*class*|*added property*|*deleted property*

|epo:Lot|generalisation -> epo:ProcurementObject|generalisation -> epo:ProcurementPart
|epo:Lot||epo:hasVariantPermission -> at-voc:permission
|epo:Lot|epo:isSubjectToLotSpecificTerm -> epo:LotSpecificTerm|epo:isSubjectToLotTerm -> epo:LotSpecificTerm
|epo:Lot|epo:usesChannel -> cpsv:Channel|epo:usesAdhoc -> cpsv:Channel
|epo:Lot|epo:foreseesContractTerm -> epo:ContractSpecificTerm|
|epo:PlannedProcurementPart|generalisation -> epo:ProcurementObject|generalisation -> epo:ProcurementPart
|epo:PlannedProcurementPart|epo:isSubjectToPlanningTerm -> epo:ProcessPlanningTerm|
|epo:Procedure|epo:isExecutedByProcurementServiceProvider -> ProcurementServiceProvider|
|epo:Procedure|epo:involvesBuyer -> epo:Buyer|
|epo:Procedure||epo:hasOptionsPermission -> at-voc:permission
|epo:Tender|epo:specifiesSubcontractors -> epo:Subcontractor|epo:specifiesSubcontractors -> epo:EconomicOperator
|epo:Contract|epo:bindsBuyer -> epo:Buyer|
|epo:Contract|epo:bindsContractor -> epo:Contractor|
|epo:ConcessionContract|generalisation -> epo:Contract|
|epo:ReviewDecision (renamed from epo:ReviewDecisionInformation)|generalisation -> ReviewObject|generalisation -> ReviewInformation
|epo:ReviewDecision (renamed from epo:ReviewDecisionInformation)|epo:hasConfirmedIrregularityType -> at-voc:irregularity-type|
|epo:ReviewDecision (renamed from epo:ReviewDecisionInformation)|epo:appliesRemedyType -> at-voc:review-remedy-type|
|epo:ReviewDecision (renamed from epo:ReviewDecisionInformation)|epo:resolvesReviewRequest -> ReviewRequest|
|epo:ReviewObject (renamed from epo:ReviewInformation)|generalisation -> epo:ProcurementObject|generalisation -> epo:ContextSpecificDescription
|epo:ReviewObject (renamed from epo:ReviewInformation)|epo:refersToPreviousReview -> epo:ReviewObject|epo:previousReview -> epo:ReviewInformation
|epo:ReviewObject (renamed from epo:ReviewInformation)||epo:hasIrregularityType -> at-voc:irregularity-type
|epo:ReviewObject (renamed from epo:ReviewInformation)||epo:reviewRemedyType -> at-voc:review-remedy-type
|epo:ReviewObject (renamed from epo:ReviewInformation)||epo:hasID -> epo:Identifier
|epo:ReviewRequest (renamed from epo:ReviewRequestInformation)|epo:hasAllegedIrregularityType -> at-voc:irregularity-type|
|epo:ReviewRequest (renamed from epo:ReviewRequestInformation)|epo:requestsRemedyType -> at-voc:review-remedy-type|
|epo:ReviewRequest (renamed from epo:ReviewRequestInformation)|epo:paidReviewRequestFee -> epo:MonetaryValue|epo:hasReviewRequestFee -> epo:MonetaryValue
|epo:ReviewRequest (renamed from epo:ReviewRequestInformation)|generalisation -> ReviewObject|generalisation -> ReviewInformation
|===

==== Agent package


|===
|*class*|*added attributes*|*deleted attributes*

|cpv:Person|dct:alternativeName|epo:hasAlternativeName
|cpv:Person|foaf:familyName|epo:hasFamilyName
|cpv:Person|foaf:name|epo:hasFullName
|cpv:Person|foaf:givenName|epo:hasGivenName
|cpv:Person|cpv:patronymicName|epo:hasPatronymicName
|===

|===
|*class*|*added attributes*|*deleted attributes*

|cpv:Person|generalisation -> foaf:Person|generalisation -> foaf:Agent
|cpv:Person|cpv:placeOfBirth -> dct:Location|
|cpv:Person|cpv:placeOfDeath -> dct:Location|
|epo:Business|epo:hasBusinessSize -> at-voc:economic-operator-size|epo:hasSize -> at-voc:economic-operator-size
|foaf:Person||generalisation -> foaf:Agent
|===

==== Role package


|===
|*class*|*added attributes*|*deleted attributes*

|epo:Buyer|epo:isResponsibleForProcedure|
|===


|===
|*class*|*added property*|*deleted property*

|epo:Winner||epo:isRoleOfBusiness -> epo:Business
|===

==== Location package

|===
|*class*|*added attributes*|*deleted attributes*

|cpov:ContactPoint|cpov:telephone|epo:hasTelephone
|cpov:ContactPoint|cpov:email|epo:hasEmail
|===

==== Term package

|===
|*class*|*added attributes*|*deleted attributes*

|epo:AccessTerm|epo:hasPublicAccessURL|
|epo:SubmissionTerm|epo:hasSubmissionURL|
|epo:ContractTerm|epo:hasOptions|
|epo:ContractTerm|epo:hasOptionsDescription|
|epo:ProcessPlanningTerm|epo:hasEstimatedTenderInvitationDate|
|epo:ProcessPlanningTerm|epo:hasEstimatedContractNoticePublicationDate|
|epo:ProcessPlanningTerm|epo:hasAwardDateScheduled|
|===

|===
|*class*|*added property*|*deleted property*

|epo:ContractSpecificTerm|generalisation -> epo:Term|
|epo:AccessTerm|epo:definesCatalogueProvider -> epo:CatalogueProvider|
|epo:AccessTerm|epo:definesCatalogueReceiver -> epo:CatalogueReceiver|
|epo:AccessTerm|epo:definesOfflineAccessProvider -> epo:OfflineAccessProvider|epo:involvesOfflineAccessProvider -> epo:OfflineAccessProvider
|epo:AccessTerm|epo:definesProcurementProcedureInformationProvider -> epo:ProcurementProcedureInformationProvider|epo:involvesProcurementProcedureInformationProvider -> epo:ProcurementProcedureInformationProvider
|epo:OpeningTerm||epo:hasVirtualTenderOpeningAddress -> cpsv:Channel
|epo:OpeningTerm|epo:definesOpeningPlace -> locn:Address|epo:hasOpeningPlace -> locn:Address
|epo:ParticipationRequestTerm|epo:definesParticipationRequestProcessor -> epo:ParticipationRequestProcessor|epo:involvesParticipationRequestProcessor -> epo:ParticipationRequestProcessor
|epo:ParticipationRequestTerm|epo:definesParticipationRequestReceiver -> epo:ParticipationRequestReceiver|epo:involvesParticipationRequestReceiver -> epo:ParticipationRequestReceiver
|epo:ReviewTerm|epo:definesReviewer -> epo:Reviewer|epo:involvesReviewer -> epo:Reviewer
|epo:ReviewTerm|epo:definesReviewProcedureInformationProvider -> ReviewProcedureInformationProvider|epo:involvesReviewProcedureInformationProvider -> ReviewProcedureInformationProvider
|epo:DirectAwardTerm|epo:refersToPreviousProcedureLot -> epo:Lot|epo:refersToPreviousProcedureLots -> epo:Lot
|epo:DirectAwardTerm|epo:refersToPreviousProcedure -> epo:Procedure|
|epo:ProcedureTerm||epo:hasClarificationsAvailableVia -> cpsv:Channel
|epo:ProcedureTerm||epo:hasQuestionsMadeAvailableVia -> cpsv:Channel
|epo:ProcedureTerm||epo:involvesBuyer -> epo:Buyer
|epo:ProcedureTerm|epo:definesMediator -> epo:Mediator|epo:involvesMediator -> epo:Mediator
|epo:ProcedureTerm|epo:definesBudgetProvider -> epo:BudgetProvider|
|epo:ProcedureTerm|epo:definesInformationProvider -> epo:TertiaryRole|
|epo:ProcedureTerm||epo:involvesProcurementServiceProvider -> epo:ProcurementServiceProvider
|epo:ProcedureTerm||epo:involves Reviewer -> epo:Reviewer
|epo:SubmissionTerm|epo:hasVariantPermission -> at-voc:permission|
|epo:SubmissionTerm||epo:hasSubmissionCommunicationMeans -> cpsv:Channel
|epo:SubmissionTerm|epo:definesTenderProcessor -> epo:TenderProcessor|epo:involvesTenderProcessor -> epo:TenderProcessor
|epo:SubmissionTerm|epo:definesTenderReceiver -> epo:TenderReceiver|epo:involvesTenderReceiver -> epo:TenderReceiver
|epo:SubcontractTerm|generalisation -> epo:ContractSpecificTerm|generalisation -> epo:LotSpecificTerm
|epo:ContractTerm|generalisation -> epo:ContractSpecificTerm|generalisation -> epo:LotSpecificTerm
|epo:ContractTerm|epo:definesSpecificPlaceOfPerformance -> dct:Location|epo:hasSpecificPlaceOfPerformance -> dct:Location
|epo:ContractTerm|epo:definesPaymentExecutor -> epo:PaymentExecutor|epo:involvesPaymentExecutor -> epo:PaymentExecutor
|epo:ContractTerm|epo:definesSubcontractingTerm -> epo:SubcontractTerm|epo:hasSubcontractTerm -> epo:SubcontractTerm
|epo:ProcessPlanningTerm|generalisation -> epo:LotSpecificTerm|
|===

==== Criterion package

|===
|*class*|*added attributes*|*deleted attributes*

|cccev:Constraint|epo:hasThresholdValue|
|cccev:Criterion|cccev:weightingConsiderationDescription|
|cccev:Criterion|cccev:weight|
|cccev:Criterion|cccev:bias|
|cccev:Requirement|cccev:name|
|cccev:Requirement|cccev:identifier|
|cccev:Requirement|cccev:description|
|epo:ExclusionGround|epo:hasPersonalSituationCondition|
|epo:ProcurementCriterion||epo:hasWeightValue
|epo:ProcurementCriterion||epo:hasWeightingJustification
|epo:ProcurementCriterion||epo:hasThresholdValue
|epo:ProcurementCriterion||epo:hasName
|epo:ProcurementCriterion||epo:hasDescription
|===

|===
|*class*|*added property*|*deleted property*

|cccev:Constraint|generalisation -> cccev:Requirement|
|cccev:Constraint|epo:hasThresholdType -> at-voc:number-threshold|
|cccev:Criterion|generalisation -> cccev:Requirement|
|cccev:Criterion|cccev:type -> at-voc:criterion|
|cccev:Requirement|cccev:hasRequirement -> cccev:Requirement|
|epo:ProcurementCriterion||epo:hasThresholdType -> at-voc:number-threshold
|===

==== Technique package

|===
|*class*|*added attributes*|*deleted attributes*

|epo:EAuctionTechnique|epo:hasEAuctionURL|
|===

|===
|*class*|*added property*|*deleted property*

|epo:EAuctionTechnique|epo:hasConstraint -> cccev:Constraint|
|===

==== Contextual description package

|===
|*class*|*added attributes*|*deleted attributes*

|epo:RecurrenceInformation|epo:hasRecurrenceDescription|
|epo:RecurrenceInformation|epo:hasRecurrence|
|epo:NoticeAwardInformation||epo:isProcurementToBeRelaunched
|epo:NoticeAwardInformation||epo:isCompetitionTerminated
|===

|===
|*class*|*added property*|*deleted property*

|epo:RecurrenceInformation|generalisation -> epo:ContextSpecificDescription|
|epo:RecurrenceInformation|epo:concernsLotRecurrence -> epo:Lot|
|epo:RecurrenceInformation|epo:concernsProcedureRecurrence -> epo:Procedure|
|epo:LotAwardOutcome|epo:hasFrameworkAgreementMaximumValue -> epo:MonetaryValue|epo:providesFrameworkAgreementMaximumValue -> epo:MonetaryValue
|epo:LotAwardOutcome|epo:hasFrameworkAgreementEstimatedValue -> epo:MonetaryValue|epo:providesFrameworkAgreementEstimatedValue -> epo:MonetaryValue
|epo:LotAwardOutcome|epo:hasAwardedValue -> epo:MonetaryValue|epo:providesAwardedValue -> epo:MonetaryValue
|epo:LotAwardOutcome|epo:hasAwardedEstimatedValue -> epo:MonetaryValue|epo:providesAwardedEstimatedValue -> epo:MonetaryValue
|epo:NoticeAwardInformation||epo:indicatesCancelledLotToBeRelaunched -> epo:Lot
|epo:TenderAwardOutcome|epo:awardsLotToWinner -> epo:Winner|epo:isAwardedToWinner -> epo:Winner
|epo:CompetitionTerminationInformation|generalisation -> epo:ContextSpecificDescription|
|epo:CompetitionTerminationInformation|epo:concernsLotCompetitionTermination -> epo:Lot|
|epo:CompetitionTerminationInformation|epo:concernsProcedureCompetitionTermination -> epo:Procedure|
|epo:StatisticalInformation|generalisation -> epo:ContextSpecificDescription|
|epo:RelaunchInformation|generalisation -> epo:ContextSpecificDescription|
|epo:RelaunchInformation|epo:concernsLotRelaunch -> epo:Lot|
|epo:RelaunchInformation|epo:concernsProcedureRelaunch -> epo:Procedure|
|===

==== Document package

|===
|*class*|*added property*|*deleted property*

|epo:CompetitionNotice||epo:announcesReviewTerm -> epo:ReviewTerm
|epo:ContractModificationNotice||epo:refersToNotice -> epo:Notice
|epo:Notice|epo:refersToNotice -> epo:Notice|
|===

==== Notice description package

|===
|*class*|*added property*|*deleted property*

|epo:PublicationProvision|epo:hasElementConfidentiality -> epo:ElementConfidentialityDescription|epo:hasFieldConfidentiality -> epo:ElementConfidentialityDescription
|===

== Pre-release ePO 3.0.0 alpha

|===
|*Metadata*|*Value*

|Reference ePO version|2.0.1
|Target ePO version|3.0.0 alpha
|Authors|Andreea Pasăre, Eugeniu Costetchi
|Date|2022-04-30
|===

=== New package organisation

The conceptual model of the ontology has been sectioned into packages for better content management. Within each package are found classes and one or several diagrams that best depicts the specific aspects of the ontology.  +
The list of content packages is as follows:

* _procurement object_
* _term_
* _agent_
* _role_
* _location_
* _contract_
* _document_
* _strategic procurement_
* _technique_
* _criteria_
* _contextual description_
* _notice description_
* _dimension_
* _controlled vocabularies_

In addition, we provide a package, called _epo diagrams_, with diagrams that provide selected views of the ontology.

=== New classes

* epo:AcquiringCentralPurchasingBody
* epo:AgentInRole
* epo:Awarder
* epo:AwardEvaluationTerm
* epo:AwardingCentralPurchasingBody
* epo:BudgetProvider
* epo:BuyerSideSignatory
* epo:CatalogueProvider
* epo:CatalogueReceiver
* epo:CompetitionNotice
* epo:CompletionNotice
* epo:ContractLotCompletionInformation
* epo:ContractorSideSignatory
* epo:ContractSignatory
* epo:Duration
* epo:ElementChangeSpecification
* epo:ElementConfidentialitySpecification
* epo:ElementDescription
* epo:Elementpecification
* epo:EmploymentInformationProvider
* epo:EnviromentalProtectionInformationProvider
* epo:GroupLeader
* epo:InformationProvider
* epo:LotAwardOutcome
* epo:LotGroupAwardInformation
* epo:LotSpecificTerm
* epo:NoticeAwardInformation
* epo:NoticeChange
* epo:NoticeDescription
* epo:OfflineAccessProvider
* epo:ParticipationRequestProcessor
* epo:ParticipationRequestReceiver
* epo:ParticipationRequestTerm
* epo:PaymentExecutor
* epo:PlanningNotice
* epo:ProcedureSpecificTerm
* epo:ProcurementObject
* epo:ProcurementPart
* epo:ProcurementProcedureInformationProvider
* epo:ResultNotice
* epo:ReviewDecisionInformation
* epo:ReviewInformation
* epo:ReviewIrregularitySummary
* epo:ReviewProcedureInformationProvider
* epo:ReviewRequester
* epo:ReviewRequestInformation
* epo:ReviewRequestSummary
* epo:SecondaryRole
* epo:SelectionEvaluationTerm
* epo:SubcontractingEstimate
* epo:SubmissionStatisticalInformation
* epo:TaxInformationProvider
* epo:TenderAwardOutcome
* epo:TenderGroup
* epo:TenderProcessor
* epo:TenderReceiver
* epo:Term
* epo:TertiaryRole
* locn:Address
* locn:Geometry

=== Deleted classes

* epo:Amount
* epo:BuyerProfileNotice
* epo:BuyerProfile
* epo:CallForCompetition
* epo:CallForExpressionOfInterest
* epo:ContractAwardNotice
* epo:ContractNotice
* epo:Item
* epo:Location
* epo:PriorInformationNotice
* epo:ProjectProcurement
* epo:ResourceElement
* epo:Subcontract
* epo:TenderDocument
* epo:TenderLot
* epo:VoluntaryEx-anteTransparencyNotice
* epo:LocationCoordinate

=== New enumerations

* at-voc:decision-type
* at-voc:irregularity-type
* at-voc:received-submission-type
* at-voc:review-remedy-type
* time:TemporalUnit

=== Deleted enumerations

* epo:cpb-type

=== Changed classes

==== Agent package

|===
|*class*|*added attributes*|*deleted attributes*

|epo:Agent||epo:ID
|epo:Agent|epo:hasName|
|epo:Organisation|epo:hasLegalName|
|epo:Organisation|epo:hasOrganisationUnit|
|===

|===
|*class*|*added property*|*deleted property*

|epo:Agent|epo:hasID -> epo:Identifier|
|epo:Organisation|epo:hasRegisteredAddress -> locn:Address|
|epo:Organisation|epo:hasAddress -> locn:Address|epo:hasLocation -> epo:Location
|epo:Organisation|epo:hasDeliveryGateway -> epo:Channel|
|epo:Organisation|epo:hasPrimaryContactPoint -> epo:ContactPoint|epo:hasDefaultContactPoint -> epo:ContactPoint
|epo:Person|epo:hasLegalLocation -> epo:Location|epo:hasRegisteredAddress -> locn:Address
|epo:Person|epo:hasCountryOfBirth -> at-voc:country|
|===

==== Procurement objects package

epo:Lot class was duplicated in ePO 2.0.1.

|===
|*class*|*added attributes*|*deleted attributes*

|epo:LotGroup||epo:Description
|epo:LotGroup||epo:ID
|epo:LotGroup||epo:Title
|epo:Lot||epo:ID
|epo:Lot||epo:PerformingStafQualificationInformation
|epo:Lot||epo:ReservedProcurement
|epo:Lot||epo:SMESuitable
|epo:Lot||epo:Title
|epo:Lot||epo:VariantsPermission
|epo:Lot||epo:Description
|epo:Lot||epo:AdditionalInformation
|epo:PlannedProcurementPart|epo:hasEstimatedContractNoticePublicationDate|
|epo:PlannedProcurementPart||epo:AdditionalInformation
|epo:PlannedProcurementPart||epo:Description
|epo:PlannedProcurementPart||epo:ID
|epo:PlannedProcurementPart||epo:LegalBasisID
|epo:PlannedProcurementPart||epo:SMESuitable
|epo:PlannedProcurementPart||epo:Title
|epo:Procedure||epo:ChoiceJustification
|epo:Procedure||epo:Description
|epo:Procedure||epo:ID
|epo:Procedure||epo:LegalBasisID
|epo:Procedure||epo:LegalBasis
|epo:Procedure||epo:LegalRegime
|epo:Procedure||epo:ProcedureType
|epo:Procedure||epo:Title
|epo:ProcurementObject|epo:hasDescription|
|epo:ProcurementObject|epo:hasTitle|
|epo:ProcurementPart|epo:hasAdditionalInformation|
|epo:ProcurementPart|epo:isSMESuitable|
|epo:ProcurementPart|epo:isUsingEUFunds|
|epo:Purpose|epo:hasRecurrenceDescription|
|epo:Purpose|epo:hasRecurrence|
|epo:Purpose|epo:hasOptions|
|epo:Purpose||epo:AdditionalClassification
|epo:Purpose||epo:AdditionalContractNature
|epo:Purpose||epo:ContractNatureType
|epo:Purpose||epo:MainClassification
|epo:Purpose||epo:OptionsPermission
|epo:Purpose||epo:hasTotalMagnitudeQuantity
|epo:Tender|epo:hasCalculationMethod|
|epo:Tender|epo:hasVariant|
|epo:Tender||epo:ID
|===

|===
|*class*|*added property*|*deleted property*

|epo:LotGroup|epo:hasID -> epo:Identifier|
|epo:LotGroup|epo:setsGroupingContextFor -> epo:Lot|
|epo:LotGroup|epo:specifiesProcurementCriteria -> epo:ProcurementCriterion|
|epo:LotGroup||epo:isAwardedTo -> epo:Tender
|epo:LotGroup||epo:hasAwardedValue -> epo:Value
|epo:LotGroup|epo:hasEstimatedValue -> epo:MonetaryValue|epo:hasEstimatedValue -> epo:Value
|epo:Lot|generalisation -> epo:ProcurementPart|
|epo:Lot||epo:isGroupedIn epo:LotGroup
|epo:Lot||epo:hasAwardedEstimatedValue -> epo:Value
|epo:Lot||epo:providesAdditionalInformation -> epo:StatisticalInformation
|epo:Lot||epo:requires -> epo:SecurityClearanceTerm
|epo:Lot|epo:hasEstimatedValue -> epo:MonetaryValue|epo:hasEstimatedValue -> epo:Value
|epo:Lot||epo:contributesToImplement -> epo:ProjectProcurement
|epo:Lot|epo:hasPurpose -> epo:Purpose|epo:has -> epo:Purpose
|epo:Lot||epo:isAwardedToTenderLot -> epo:TenderLot
|epo:Lot||epo:has -> epo:OpeningTerm
|epo:Lot||epo:involvesOverallStrategicProcurement -> epo:strategicProcurement
|epo:Lot|epo:hasPerformingStaffQualificationInformation -> at-voc:requirement-stage|epo:isProvidedWithin -> at-voc:requirement-stage
|epo:Lot||epo:hasEstimatedUserConcessionRevenue -> epo:Value
|epo:Lot||epo:applies -> epo:MultipleStageProcedureTerm
|epo:Lot||epo:applies -> epo:ContractTerm
|epo:Lot||epo:hasTenderEvaluationTerm -> epo:EvaluationTerm
|epo:Lot||epo:hasContractDuration -> epo:Period
|epo:Lot||epo:hasEstimatedBuyerConcessionRevenue -> epo:Value
|epo:Lot|epo:refersToPlannedPart -> epo:PlannedProcurementPart|epo:refersTo -> epo:PlannedProcurementPart
|epo:Lot||epo:isReferredToIn -> epo:ProcurementDocument
|epo:Lot||epo:hasAwardedValue -> epo:Value
|epo:Lot||epo:refersTo -> epo:Item
|epo:Lot||epo:isFundedBy -> epo:Fund
|epo:Lot|epo:isSubjectToLotTerm -> epo:LotSpecificTerm|
|epo:Lot|epo:usesTechnique -> epo:Technique|epo:uses -> epo:Technique
|epo:Lot|epo:specifiesProcurementCriteria -> epo:ProcurementCriterion|
|epo:PlannedProcurementPart|generalisation -> epo:ProcurementPart|
|epo:PlannedProcurementPart|epo:hasLegalBasis -> at-voc:legal-basis|epo:hasLegalBasisID -> at-voc:legal-basis
|epo:PlannedProcurementPart|epo:usesChannel -> epo:Channel|epo:uses -> epo:Channel
|epo:PlannedProcurementPart|epo:hasPlannedDuration -> epo:Duration|
|epo:PlannedProcurementPart||epo:has -> epo:AccessTerm
|epo:PlannedProcurementPart||epo:has -> epo:ContractTerm
|epo:PlannedProcurementPart||epo:involvesOverallStrategicProcurement -> epo:StrategicProcurement
|epo:PlannedProcurementPart||epo:refersTo -> epo:Document
|epo:PlannedProcurementPart||epo:isFundedWith -> epo:Fund
|epo:Procedure|epo:isSubjectToProcedureSpecificTerm -> epo:ProcedureSpecificTerm|epo:has -> epo:ProcedureTerm
|epo:Procedure|epo:refersToPlannedPart -> epo:PlannedProcurementPart|
|epo:Procedure|epo:hasEstimatedValue -> epo:MonetaryValue|epo:hasEstimatedValue -> epo:Value
|epo:Procedure|generalisation -> epo:ProcurementObject|
|epo:Procedure|epo:hasProcurementScopeDividedIntoLot -> epo:Lot|epo:specifies -> epo:Lot
|epo:Procedure|epo:specifiesExclusionGround -> epo:ExclusionGround|epo:uses -> epo:ExclusionGround
|epo:Procedure||epo:involvesOverallStrategicProcurement -> epo:StrategicProcurement
|epo:Procedure||epo:leadsTo -> epo:Contract
|epo:Procedure||epo:isResponsabilityOf -> epo:Buyer
|epo:Procedure||epo:isConcludedBy -> epo:Contract
|epo:Procedure||epo:uses -> epo:AccessTerm
|epo:Procedure||epo:has -> epo:DirectAwardTerm
|epo:Procedure||epo:hasTotalValue -> epo:Value
|epo:ProcurementObject|epo:isSubjectToTerm -> epo:Term|
|epo:ProcurementObject|epo:fulfillStrategicProcurement -> epo:StrategicProcurement|
|epo:ProcurementObject|epo:hasID -> epo:Identifier|
|epo:ProcurementPart|generalisation -> epo:ProcurementObject|
|epo:ProcurementPart|epo:isFundedBy -> epo:Fund|
|epo:Purpose|epo:hasTotalQuantity -> epo:Quantity|
|epo:TenderGroup|epo:comprisesTender -> epo:Tender|
|epo:TenderGroup|epo:hasTotalValue -> epo:MonetaryValue|
|epo:TenderGroup|epo:isSubmittedForLotGroup -> epo:LotGroup|
|epo:Tender|epo:isSupportedBy -> epo:TechnicalOffer|
|epo:Tender|epo:isSubmittedForLot -> epo:Lot|
|epo:Tender|epo:hasItemCountryOfOrigin -> at-voc:country|
|epo:Tender|epo:subjectToGrouping -> epo:LotGroup|
|epo:Tender|epo:foreseesSubcontractingEstimate -> epo:SubcontractingEstimate|
|epo:Tender|epo:hasEstimatedUserConcessionRevenue -> epo:MonetaryValue|
|epo:Tender|generalisation -> epo:ProcurementObject|
|epo:Tender|epo:hasEstimatedBuyerConcessionRevenue -> epo:MonetaryValue|
|epo:Tender|epo:hasFinancialOfferValuer -> epo:MonetaryValue|
|epo:Tender|epo:isSupportedBy -> epo:ESPDResponse|
|epo:Tender|epo:isSupportedBy -> epo:FinancialOffer|
|epo:Tender||epo:attaches -> epo:TenderDocument
|epo:Tender||epo:includes -> epo:TenderLot
|epo:Tender||epo:hasSubmissionTerm -> epo:SubmissionTerm
|===

==== Roles package

|===
|*class*|*added attributes*|*deleted attributes*

|epo:AgentInRole|epo:hasDescription|
|epo:AgentInRole|epo:hasTitle|
|epo:Buyer|epo:hasBuyerTypeDescription|epo:BuyerLegalTypeDescription
|epo:Buyer|epo:hasBuyerProfile|
|epo:Buyer||epo:hasBuyerLegalType
|epo:Buyer||epo:MainActivityType
|epo:CentralPurchasingBody||epo:CPBType
|epo:EconomicOperator||epo:EORoleType
|===

|===
|*class*|*added property*|*deleted property*

|epo:AcquiringCentralPurchasingBody|generalisation -> epo:CentralPurchasingBody|
|epo:AgentInRole|epo:playedBy -> epo:Agent|
|epo:AgentInRole|epo:dependsOnRole -> epo:AgentInRole|
|epo:AgentInRole|epo:hasContactPointInRole -> epo:ContactPoint|
|epo:Awarder|epo:dependsOnBuyer -> epo:Buyer|
|epo:Awarder|generalisation -> epo:PrimaryRole|
|epo:AwardingCentralPurchasingBody|generalisation -> epo:CentralPurchasingBody|
|epo:BudgetProvider|epo:dependsOnServiceProvider -> epo:ProcurementServiceProvider|
|epo:BudgetProvider|generalisation -> epo:SecondaryRole|
|epo:BudgetProvider|epo:dependsOnBuyer -> epo:Buyer|
|epo:BuyerSideSignatory|epo:dependsOnBuyer -> epo:Buyer|
|epo:BuyerSideSignatory|generalisation -> epo:ContractSignatory|
|epo:Buyer|epo:hasBuyerType -> at-voc:buyer-legal-type|epo:hasBuyerLegalType -> at-voc:buyer-legal-type
|epo:Buyer|epo:delegatesAncillaryActivitiesTo -> epo:ProcurementServiceProvider|
|epo:Buyer||epo:executesPayment -> epo:Lot
|epo:Buyer||epo:processesTenders -> epo:Lot
|epo:Buyer||epo:has -> epo:BuyerProfile
|epo:Buyer||epo:processesRequestsToParticipate -> epo:Lot
|epo:Buyer||generalisation -> epo:Role
|epo:Buyer||epo:providesMoreInformationOnTimeLimitsForReviewProcedures -> epo:Lot
|epo:Buyer||epo:receivesRequestsToParticipate -> epo:Lot
|epo:Buyer||epo:isGroupLeader -> epo:Lot
|epo:Buyer||epo:appoints -> epo:EvaluationBoard
|epo:Buyer||epo:makesDecision -> epo:AwardDecision
|epo:Buyer||epo:providesAdditionalInformationAboutProcurementProcedure -> epo:Lot
|epo:Buyer||epo:usesBudgetToPayContract -> epo:Lot
|epo:Buyer||epo:receivesTenders -> epo:Lot
|epo:Buyer||epo:providesOfflineAccessToProcurementDocuments -> epo:Lot
|epo:Buyer||epo:plans -> epo:PlannedProcurementPart
|epo:Buyer||epo:signsContract -> epo:Lot
|epo:CatalogueProvider|generalisation -> epo:EconomicOperator|
|epo:CatalogueReceiver|generalisation -> epo:PrimaryRole|
|epo:CentralPurchasingBody|epo:hasCentralPurchasingBody -> epo:cpb-type|
|epo:ContractSignatory|generalisation -> epo:SecondaryRole|
|epo:ContractorSideSignatory|generalisation -> epo:ContractSignatory|
|epo:ContractorSideSignatory|epo:dependsOnWinner -> epo:Winner|
|epo:Contractor|generalisation -> epo:EconomicOperator|generalisation -> epo:Winner
|epo:Contractor|epo:dependsOnContractorSideSignatory -> epo:ContractorSideSignatory|
|epo:EconomicOperator|epo:playedByBusiness epo:Business|
|epo:EmploymentInformationProvider|generalisation -> epo:TertiaryRole|
|epo:EnvironmentalProtectionInformationProvider|generalisation -> epo:TertiaryRole|
|epo:GroupLeader|generalisation -> epo:SecondaryRole|
|epo:InformationProvider|generalisation -> epo:SecondaryRole|
|epo:InformationProvider|epo:dependsOnBuyer -> epo:Buyer|
|epo:InformationProvider|epo:dependsOnServiceProvider -> epo:ProcurementServiceProvider|
|epo:OfflineAccessProvider|generalisation -> epo:InformationProvider|
|epo:ParticipationRequestProcessor|epo:dependsOnServiceProvider -> epo:ProcurementServiceProvider|
|epo:ParticipationRequestProcessor|epo:dependsOnBuyer -> epo:Buyer|
|epo:ParticipationRequestProcessor|generalisation -> epo:SecondaryRole|
|epo:ParticipationRequestReceiver|epo:dependsOnServiceProvider -> epo:ProcurementServiceProvider|
|epo:ParticipationRequestReceiver|epo:dependsOnBuyer -> epo:Buyer|
|epo:ParticipationRequestReceiver|generalisation -> epo:SecondaryRole|
|epo:PaymentExecutor|epo:dependsOnServiceProvider -> epo:ProcurementServiceProvider|
|epo:PaymentExecutor|epo:dependsOnBuyer -> epo:Buyer|
|epo:PaymentExecutor|generalisation -> epo:SecondaryRole|
|epo:ProcurementProcedureInformationProvider|generalisation -> epo:InformationProvider|
|epo:ProcurementServiceProvider|epo:actsOnBehalfOf -> epo:Buyer|
|epo:ProcurementServiceProvider||epo:receivesRequestsToParticipate -> epo:Lot
|epo:ProcurementServiceProvider||epo:providesAdditionalInformationAboutProcurementProcedure -> epo:Lot
|epo:ProcurementServiceProvider||epo:isGroupLeader -> epo:Lot
|epo:ProcurementServiceProvider||epo:executesPayment -> epo:Lot
|epo:ProcurementServiceProvider||epo:manages -> epo:BuyerProfile
|epo:ProcurementServiceProvider||epo:processesTenders -> epo:Lot
|epo:ProcurementServiceProvider||epo:processesRequestsToParticipate -> epo:Lot
|epo:ProcurementServiceProvider||epo:providesMoreInformationOnTimeLimitsForReviewProcedures -> epo:Lot
|epo:ProcurementServiceProvider||epo:usesBudgetToPayContract -> epo:Lot
|epo:ProcurementServiceProvider||epo:receivesTenders -> epo:Lot
|epo:ProcurementServiceProvider||epo:providesOfflineAccessToProcurementDocuments -> epo:Lot
|epo:ProcurementServiceProvider||epo:signsContract -> epo:Lot
|epo:ReviewProcedureInformationProvider|epo:dependsOnReviewer -> epo:Reviewer|
|epo:ReviewProcedureInformationProvider|generalisation -> epo:InformationProvider|
|epo:ReviewRequester|generalisation -> epo:PrimaryRole|
|epo:Reviewer||epo:providesMoreInformationOnTimeLimitsForReviewProcedures -> epo:Lot
|epo:PrimaryRole|epo:playedByOrganisation -> epo:Organisation|
|epo:PrimaryRole|generalisation -> epo:AgentInRole|
|epo:PrimaryRole||epo:has -> epo:ContactPoint
|epo:SecondaryRole|generalisation -> epo:AgentInRole|
|epo:TaxInformationProvider|generalisation -> epo:TertiaryRole|
|epo:TenderProcessor|epo:dependsOnServiceProvider -> epo:ProcurementServiceProvider|
|epo:TenderProcessor|epo:dependsOnBuyer -> epo:Buyer|
|epo:TenderProcessor|generalisation -> epo:SecondaryRole|
|epo:TenderReceiver|epo:dependsOnServiceProvider -> epo:ProcurementServiceProvider|
|epo:TenderReceiver|epo:dependsOnBuyer -> epo:Buyer|
|epo:TenderReceiver|generalisation -> epo:SecondaryRole|
|epo:Tenderer|epo:substantiatesExclusionGround -> epo:ExclusionGround|epo:substantiates -> epo:ExclusionGround
|epo:Tenderer||epo:withdraws -> epo:Tender
|epo:Tenderer||epo:submits -> epo:Tender
|epo:TertiaryRole|generalisation -> epo:InformationProvider|
|epo:TertiaryRole|epo:providesRegulatoryInformation -> epo:RegulatoryFrameworkInformation|
|epo:Winner|epo:dependsOnTenderer -> epo:Tenderer|
|epo:Winner|generalisation -> epo:EconomicOperator|generalisation -> epo:Tenderer
|===

==== Location package

|===
|*class*|*added attributes*|*deleted attributes*

|locn:Address|locn:postName|epo:CityName
|locn:Address|locn:postCode|epo:PostalZone
|locn:Address|locn:thoroughfare|epo:StreetName
|locn:Address|locn:adressArea|
|locn:Address|locn:FullAddress|
|locn:Address|locn:locatorDesignator|
|locn:Address|locn:locatorName|
|locn:Address||epo:AdditionalStreetName
|locn:Address||epo:BlockName
|locn:Address||epo:BuildingName
|locn:Address||epo:BuildingNumber
|locn:Address||epo:CitySubdivisionName
|locn:Address||epo:CountryCode
|locn:Address||epo:CountrySubentityCode
|locn:Address||epo:CountrySubentity
|locn:Address||epo:District
|locn:Address||epo:Floor
|locn:Address||epo:ID
|locn:Address||epo:InhouseMail
|locn:Address||epo:MarkAttention
|locn:Address||epo:PlotIdentification
|locn:Address||epo:PostBox
|locn:Address||epo:Region
|locn:Address||epo:Room
|locn:Address||epo:TimezoneOffset
|epo:ContactPoint|epo:hasContactName|
|dct:Location|locn:geographicName|
|locn:Geometry|locn:latitude|
|locn:Geometry|locn:longitude|
|locn:Geometry|locn:coordinates|
|===

|===
|*class*|*added property*|*deleted property*

|locn:Address|locn:adminUnitL2 -> at-voc:nuts|epo:hasCountrySubentityCode -> at-voc:nuts
|locn:Address|locn:addressID -> epo:Identifier|
|locn:Address|locn:adminUnitL1 -> at-voc:country|epo:hasCountryCode -> at-voc:country
|locn:Address||epo:has -> epo:LocationCoordinate
|epo:ContactPoint|epo:hasAddress -> locn:Address|epo:hasLocation -> epo:Location
|epo:ContactPoint|generalisation -> epo:CommunicationMeans|
|epo:ContactPoint||epo:has -> epo:Channel
|epo:ContactPoint||epo:hasContactPersonRole -> epo:Role
|dct:Location|epo:hasCountryCode -> at-voc:country|
|dct:Location|epo:hasNutsCode -> at-voc:nuts|
|dct:Location|locn:geographicIdentifier -> epo:Identifier|
|dct:Location|locn:geometry -> locn:Geometry|
|dct:Location|locn:address -> locn:Address|
|dct:Location||epo:hasPostalAddress -> epo:Address
|===

==== Contract package

|===
|*class*|*added attributes*|*deleted attributes*

|epo:Contract|epo:hasAccessAddress|
|epo:Contract|epo:hasWinnerDecisionDate|
|epo:Contract||epo:ID
|epo:Contract||epo:Title
|epo:Fund||epo:ID
|epo:PurchaseContract|epo:isWithinFrameworkAgreement|
|===

|===
|*class*|*added property*|*deleted property*

|epo:Contract|epo:includesLot -> epo:Lot|
|epo:Contract|epo:signedBySignatory -> epo:ContractSignatory|
|epo:Contract|epo:includesLotAwardOutcome -> epo:LotAwardOutcome|
|epo:Contract|epo:hasEstimatedDuration -> epo:Duration|epo:hasEstimatedDuration -> epo:Period
|epo:Contract|epo:includesTender -> epo:Tender|
|epo:Contract|generalisation -> epo:ProcurementObject|
|epo:Contract||epo:refersTo -> epo:Lot (epo:isReferredByA -> epo:Contract)
|epo:Contract||epo:attaches -> epo:Document
|epo:Contract||epo:isSignedBy -> epo:Agent (epo:isSignatoryPartyOf -> epo:Contract)
|epo:Contract||epo:refersToSignatory -> epo:Winner
|epo:Contract||epo:hasDuration -> epo:Period
|epo:Contract||epo:mentions -> epo:LotGroup
|epo:Contract||epo:refersTo -> epo:Tender
|epo:Contract||generalisation -> epo:Document
|epo:Contract||epo:hasProcurementValue -> epo:Value
|epo:Contract||epo:hasDurationEvaluationPeriod -> epo:Period
|epo:Contract||epo:hasContractPurpose -> epo:Purpose
|epo:Fund|epo:hasID -> epo:Identifier|
|epo:PurchaseContract|epo:followsRulesSetBy -> epo:FrameworkAgreement|epo:hasRulesSetBy -> epo:FrameworkAgreement (epo:setsRulesOf -> epo:PurchaseContract)
|===

==== Term package

|===
|*class*|*added attributes*|*deleted attributes*

|epo:AccessTerm|epo:isProcurementDocumentRestricted|epo:SomeProcurementDocumentRestricted
|epo:AccessTerm|epo:hasRestrictedAccessURL|
|epo:AccessTerm||epo:ProcurementDocumentLandingPage
|epo:AccessTerm||epo:SomeProcurementDocumentRestrictedJustification
|epo:Channel|epo:isAtypical|
|epo:ContractTerm||epo:BroadPlaceOfPerformance
|epo:ContractTerm||epo:ReservedExecution
|epo:FrameworkAgreementTerm||epo:FrameworkAgreementType
|epo:MultipleStageProcedureTerm||epo:MaximumCandidates
|epo:Prize||epo:PrizeValue
|epo:SubcontractTerm||epo:SubcontractingObligation
|epo:AwardEvaluationTerm|epo:hasAwardEvaluationFormula (from epo:EvaluationTerm)|
|epo:AwardEvaluationTerm|epo:hasOverallCostAwardCriteriaPonderation (from epo:EvaluationTerm)|
|epo:AwardEvaluationTerm|epo:hasOverallPriceAwardCriteriaPonderation (from epo:EvaluationTerm)|
|epo:AwardEvaluationTerm|epo:hasOverallQualityAwardCriteriaPonderation (from epo:EvaluationTerm)|
|epo:AwardEvaluationTerm|epo:hasAwardCriteriaOrderJustification|
|epo:DirectAwardTerm||epo:JustificationType
|epo:ProcedureTerm||epo:AdditionalInformationDeadline
|epo:SubmissionTerm||epo:ECataloguePermission
|epo:SubmissionTerm||epo:ESubmissionPermission
|epo:SubmissionTerm||epo:Language
|epo:SubmissionTerm||epo:LateSubmissionPermission
|epo:SubmissionTerm||epo:NonElectronicSubmissionJustification
|epo:SubmissionTerm||epo:TenderSubcontractingInformation
|===

|===
|*class*|*added property*|*deleted property*

|epo:AccessTerm|epo:involvesInformationProvider -> epo:ProcurementProcedureInformationProvider|
|epo:AccessTerm|epo:hasProcurementDocumentLandingPage -> epo:Channel|
|epo:AccessTerm|epo:involvesProcurementDocument -> epo:ProcurementDocument|
|epo:AccessTerm|epo:involvesInformationProvider -> epo:OfflineAccessProvider|
|epo:AccessTerm|generalisation -> epo:LotSpecificTerm|
|epo:AccessTerm|epo:refersToPlannedPart -> epo:PlannedProcurementPart|
|epo:AccessTerm|epo:hasDocumentRestrictionJustification -> at-voc:communication-justification|
|epo:Channel|generalisation -> epo:CommunicationMeans|
|epo:OpeningTerm|generalisation -> epo:LotSpecificTerm|
|epo:SecurityClearanceTerm|generalisation -> epo:LotSpecificTerm|
|epo:SecurityClearanceTerm||epo:appliesTo -> org:Site
|epo:SecurityClearanceTerm||epo:appliesTo -> epo:Winner
|epo:SecurityClearanceTerm||epo:appliesTo -> epo:Document
|epo:ContractTerm|epo:involvesPaymentExecutor -> epo:PaymentExecutor|
|epo:ContractTerm|epo:involvesBudgetProvider -> epo:BudgetProvider|
|epo:ContractTerm|epo:hasSpecificPlaceOfPerformance -> dct:Location|epo:hasSpecificPlaceOfPerformance -> epo:Address
|epo:ContractTerm|generalisation -> epo:LotSpecificTerm|
|epo:ContractTerm|epo:hasSubcontractingTerm -> epo:SubcontractTerm|epo:includes -> epo:SubcontractTerm
|epo:DesignContestRegimeTerm|generalisation -> epo:LotSpecificTerm|
|epo:DesignContestRegimeTerm||epo:appliesTo -> epo:Lot
|epo:FrameworkAgreementTerm|generalisation -> epo:ProcedureSpecificTerm|
|epo:FrameworkAgreementTerm|generalisation -> epo:LotSpecificTerm|
|epo:FrameworkAgreementTerm||epo:appliesTo -> epo:Lot
|epo:FrameworkAgreementTerm||epo:isUsedBy -> epo:LotGroup
|epo:MultipleStageProcedureTerm|generalisation -> epo:LotSpecificTerm|
|epo:Prize|epo:hasPrizeValue -> epo:MonetaryValue|
|epo:SubcontractTerm|generalisation -> epo:LotSpecificTerm|
|epo:AwardEvaluationTerm|generalisation -> epo:EvaluationTerm|
|epo:SelectionEvaluationTerm|generalisation -> epo:EvaluationTerm|
|epo:EvaluationTerm|generalisation -> epo:LotSpecificTerm|
|epo:ParticipationRequestTerm|epo:involvesParticipationRequestReceiver -> epo:ParticipationRequestReceiver|
|epo:ParticipationRequestTerm|generalisation -> epo:LotSpecificTerm|
|epo:ParticipationRequestTerm|epo:involvesParticipationRequestProcessor -> epo:ParticipationRequestProcessor|
|epo:DirectAwardTerm|generalisation -> epo:ProcedureSpecificTerm|
|epo:ProcedureTerm|epo:involvesReviewer -> epo:Reviewer|
|epo:ProcedureTerm|epo:involvesMediator -> epo:Mediator|
|epo:ProcedureTerm|epo:involvesProcurementServiceProvider -> epo:ProcurementServiceProvider|
|epo:ProcedureTerm|epo:definesLotGroup -> epo:LotGroup|epo:combinesLotsInto -> epo:LotGroup
|epo:ProcedureTerm|generalisation -> epo:ProcedureSpecificTerm|
|epo:ProcedureTerm|epo:involvesBuyer -> epo:Buyer|
|epo:ReviewTerm|epo:involvesReviewProcedureInformationProvider -> epo:ReviewProcedureInformationProvider|
|epo:ReviewTerm|generalisation -> epo:LotSpecificTerm|
|epo:ReviewTerm||epo:isAppliedBy -> epo:Lot
|epo:SubmissionTerm|epo:involvesTenderReceiver -> epo:TenderReceiver|
|epo:SubmissionTerm|generalisation -> epo:LotSpecificTerm|
|epo:SubmissionTerm|epo:involvesTenderProcessor -> epo:TenderProcessor|
|epo:SubmissionTerm||epo:isAppliedBy -> epo:Lot
|epo:LotSpecificTerm|generalisation -> epo:Term|
|epo:ProcedureSpecificTerm|generalisation -> epo:Term|
|===

==== Document package

|===
|*class*|*added attributes*|*deleted attributes*

|epo:AwardDecision||epo:AwardDecisionDate
|epo:AwardDecision||epo:AwardStatus
|epo:AwardDecision||epo:Justification
|epo:AwardDecision||epo:NonAwardJustification
|epo:Document|epo:hasPublicationDate (from epo:Notice)|
|epo:Document|epo:hasAccessURL|
|epo:Document|epo:hasVersion|
|epo:Document||epo:ID
|epo:Document||epo:OfficialLanguage
|epo:Document||epo:RestrictedCommunicationJustification
|epo:Document||epo:UUID
|epo:Document||epo:UnofficialLanguage
|epo:ProcurementDocument||epo:FreeEAccess
|epo:ContractModificationNotice||epo:ModificationReason
|epo:Notice||epo:DPSScope
|epo:Notice||epo:FormType
|epo:Notice||epo:NotificationContentType
|===

|===
|*class*|*added property*|*deleted property*

|epo:AwardDecision|generalisation -> epo:Document|
|epo:AwardDecision|epo:announcesLotAwardOutcome -> epo:LotAwardOutcome|
|epo:AwardDecision||epo:hasWinning -> epo:TenderLot
|epo:AwardDecision||epo:hasAwardStatus -> at-voc:winner-selection-status
|epo:AwardDecision||epo:isReferredByA -> epo:Contract
|epo:AwardDecision||epo:has -> epo:Winner
|epo:AwardDecision||epo:refersTo -> epo:Lot
|epo:AwardDecision||epo:refersTo -> epo:LotGroup
|epo:AwardDecision||epo:hasNonAwardJustification -> at-voc:non-award-justification
|epo:Document|epo:hasUUID -> epo:Identifier|
|epo:Document|epo:associatedWith -> epo:Document|
|epo:Document|epo:hasID -> epo:Identifier|
|epo:Document||epo:hasRestrictedCommunicationJustification -> at-voc:communication-justification
|epo:Document||epo:IsMadeAvailableVia -> epo:Channel
|epo:Document||epo:hasChange -> epo:Change
|epo:Document||epo:changeRefersToInstance -> epo:Document
|epo:Document||epo:relatesTo -> epo:Procedure
|epo:Document||epo:submitsDocument -> epo:Document
|epo:Document||epo:includes -> epo:RegulatoryFrameworkInformation
|epo:ExpressionOfInterest|generalisation -> epo:Document|generalisation ->TenderDocument
|epo:RequestForClarification|generalisation -> epo:Document|generalisation ->TenderDocument
|epo:RequestForParticipation|generalisation -> epo:Document|generalisation ->TenderDocument
|epo:CompetitionNotice|epo:announcesLot -> epo:Lot|
|epo:CompetitionNotice|epo:announcesLotGroup -> epo:LotGroup|
|epo:CompetitionNotice|epo:announcesRole -> epo:AgentInRole|
|epo:CompetitionNotice|generalisation -> epo:Notice|
|epo:CompetitionNotice|epo:announcesProcedure -> epo:Procedure|
|epo:CompletionNotice|generalisation -> epo:Notice|
|epo:ContractModificationNotice|epo:refersToContractToBeModified -> epo:Contract|epo:modifies -> epo:Contract
|epo:ContractModificationNotice|epo:refersToNotice -> epo:Notice|epo:refersTo -> epo:ContractAwardNotice
|epo:DirectAwardPrenotificationNotice|epo:announcesProcedure -> epo:Procedure|
|epo:DirectAwardPrenotificationNotice|generalisation -> epo:Notice|
|epo:PlanningNotice|generalisation -> epo:Notice|
|epo:ResultNotice|epo:announcesNonPublishedElement -> epo:PublicationProvision (from epo:Document)|
|epo:ResultNotice|epo:announcesLotAwardOutcome -> epo:LotAwardOutcome|
|epo:ResultNotice|epo:refersToProcedureTerm -> epo:ProcedureTerm|
|epo:ResultNotice|epo:refersToLot -> epo:Lot|
|epo:ResultNotice|epo:refersToRole -> epo:AgentInRole|
|epo:ResultNotice|epo:refersToProcedure -> epo:Procedure|
|epo:ResultNotice|generalisation -> epo:Notice|
|epo:ResultNotice|epo:announcesTender -> epo:Tender|
|epo:ResultNotice|epo:refersToLotGroup -> epo:LotGroup|
|epo:ResultNotice|epo:announcesContract -> epo:Contract|
|epo:ResultNotice|epo:announcesNoticeAwardInformation -> epo:NoticeAwardInformation|
|epo:ResultNotice|epo:announcesLotGroupAwardInformation -> epo:LotGroupAwardInformation|
|epo:Notice|epo:hasNotificationContentType -> epo:notification-phases-content-types|epo:hasNotificationPhasesType -> epo:notification-phases-content-types
|epo:Notice||epo:notifies -> epo:Procedure (epo:isNotifiedThrough -> epo:Notice)
|epo:Notice||epo:relatesToNotice -> epo:Notice
|===

==== Strategic procurement package

|===
|*class*|*added attributes*|*deleted attributes*

|epo:GreenProcurement|epo:hasCleanVehicles (from epo:StatisticalInformation)|epo:FulfillsRequirement
|epo:GreenProcurement|epo:hasTotalVehicles (from epo:StatisticalInformation)|
|epo:GreenProcurement|epo:hasTotalVehicles (from epo:StatisticalInformation)|
|epo:InnovativeProcurement||epo:FulfillsRequirement
|epo:SocialProcurement||epo:FulfillsRequirement
|epo:StrategicProcurement|epo:hasNonAccessibilityCriterionJustification (from epo:TechnicalSpecification)|
|===

|===
|*class*|*added property*|*deleted property*

|epo:StrategicProcurement|epo:includesAccessibilityCriterion -> at-voc:accessibility (from epo:TechnicalSpecification)|
|epo:StrategicProcurement||epo:isSpecifiedIn -> epo:ResourceElement
|===

==== Criterion package

|===
|*class*|*added attributes*|*deleted attributes*

|epo:AwardCriterion||epo:hasFixedValue
|epo:AwardCriterion||epo:AwardCriterionType
|epo:AwardCriterion||epo:Description
|epo:AwardCriterion||epo:FixedValueType
|epo:AwardCriterion||epo:Formula
|epo:AwardCriterion||epo:ID
|epo:AwardCriterion||epo:ThresholdType
|epo:AwardCriterion||epo:ThresholdValue
|epo:AwardCriterion||epo:WeightValueType
|epo:AwardCriterion||epo:WeightValue
|epo:AwardCriterion||epo:WeightingJustification
|epo:ProcurementCriterion|epo:hasFormula (from epo:SelectionCriterion)|
|epo:ProcurementCriterion|epo:hasThresholdValue (from epo:SelectionCriterion)|
|epo:ProcurementCriterion|epo:hasWeightingJustification (from epo:SelectionCriterion)|
|epo:ProcurementCriterion|epo:hasWeightValue (from epo:SelectionCriterion)|
|epo:ProcurementCriterion||epo:ID
|epo:SelectionCriterion||epo:SelectionCriterionType
|epo:SelectionCriterion||epo:ThresholdType
|epo:SelectionCriterion||epo:WeightValueType
|epo:EAuctionTechnique||epo:EAuctionUsage
|===

|===
|*class*|*added property*|*deleted property*

|epo:AwardCriterion||epo:hasWeightValueType -> at-voc:number-weight
|epo:AwardCriterion||epo:hasThresholdType -> at-voc:number-threshold
|epo:AwardCriterion||epo:isUsedToAward -> epo:Lot
|epo:AwardCriterion||epo:isUsedToAward -> epo:LotGroup
|epo:ExclusionGround||generalisation -> epo:ProcurementCriterion
|epo:ProcurementCriterion|epo:hasWeightValueType -> at-voc:number-weight (from epo:AwardCriterion)|
|epo:ProcurementCriterion|epo:hasThresholdType -> at-voc:number-threshold (from epo:AwardCriterion)|
|epo:SelectionCriterion|epo:hasSelectionCriteriaUsage -> at-voc:usage|
|epo:SelectionCriterion||epo:appliesTo -> epo:LotGroup
|epo:SelectionCriterion||epo:hasWeightValueType -> at-voc:number-weight
|epo:SelectionCriterion||epo:isAppliedBy -> epo:Lot (epo:specifies -> epo:SelectionCriterion)
|epo:SelectionCriterion||epo:hasThresholdType -> at-voc:number-threshold
|epo:SelectionCriterion||epo:usedForReductionOfCandidates -> epo:Lot
|===

==== Technique package

|===
|*class*|*added attributes*|*deleted attributes*

|epo:FrameworkAgreementTechnique|epo:hasFrameworkBuyerCategory|
|epo:FrameworkAgreementTechnique|epo:hasFrameworkDurationJustification|
|epo:FrameworkAgreementTechnique|epo:hasMaximumParticipantsNumber|
|epo:Technique||epo:ID
|===

|===
|*class*|*added property*|*deleted property*

|epo:DynamicPurchaseSystemTechnique|epo:hasDPSScope -> at-voc:dps-usage (from epo:Notice)|
|epo:EAuctionTechnique|epo:isAvailableViaChannel -> epo:Channel|
|epo:FrameworkAgreementTechnique||epo:isOrganisedIn -> epo:LotGroup (epo:uses -> epo:FrameworkAgreementTechnique)
|epo:FrameworkAgreementTechnique||epo:uses -> epo:EAuctionTechnique
|epo:FrameworkAgreementTechnique||epo:isConcludedBy -> epo:FrameworkAgreement
|epo:Technique||epo:isAvailableVia -> epo:Channel
|epo:Technique||epo:isUsedBy -> epo:Lot
|===

==== Contextual description package

|===
|*class*|*added attributes*|*deleted attributes*

|epo:LotAwardOutcome|epo:hasAdditionalNonAwardJustification|
|epo:LotAwardOutcome|epo:hasAwardDecisionDate|
|epo:NoticeAwardInformation|epo:isCompetitionTerminated|
|epo:NoticeAwardInformation|epo:isProcurementToBeRelaunched|
|epo:TenderAwardOutcome|epo:hasAwardRank|
|epo:ReviewInformation|epo:hasReviewDate|
|epo:ReviewInformation|epo:hasReviewDescription|
|epo:ReviewInformation|epo:hasReviewTitle|
|epo:ReviewInformation|epo:hasReviewURL|
|epo:ReviewRequestInformation|epo:hasNumberOfReviewRequests|
|epo:ReviewRequestInformation|epo:isWithdrawn|
|epo:ReviewRequestInformation|epo:hasWithdrawalDate|
|epo:ReviewRequestInformation|epo:hasWithdrawalReason|
|epo:ReviewIrregularitySummary|epo:hasReviewIrregularityCount|
|epo:ReviewRequestSummary|epo:hasTotalNumberOfComplainants|
|epo:SubmissionStatisticalInformation|epo:hasAbnormallyLowTenders (from epo:StatisticalInformation)|epo:AbnormallyLowTenderLots (from epo:StatisticalInformation)
|epo:SubmissionStatisticalInformation|epo:hasEEAReceivedTenders (from epo:StatisticalInformation)|epo:EEAReceivedTenderLots (from epo:StatisticalInformation)
|epo:SubmissionStatisticalInformation|epo:hasElectronicTenders (from epo:StatisticalInformation)|epo:ElectronicTenderLots (from epo:StatisticalInformation)
|epo:SubmissionStatisticalInformation|epo:hasInadmissibleTenders (from epo:StatisticalInformation)|epo:InadmissibleTenderLots (from epo:StatisticalInformation)
|epo:SubmissionStatisticalInformation|epo:hasMediumTenderPerLots (from epo:StatisticalInformation)|epo:MediumTenderPerLots (from epo:StatisticalInformation)
|epo:SubmissionStatisticalInformation|epo:hasNumberOfTenderersInvited (from epo:StatisticalInformation)|epo:NumberOfTenderersInvited (from epo:StatisticalInformation)
|epo:SubmissionStatisticalInformation|epo:hasReceivedMicroTenders (from epo:StatisticalInformation)|epo:ReceivedMicroTenderLots (from epo:StatisticalInformation)
|epo:SubmissionStatisticalInformation|epo:hasReceivedNonEEATenders (from epo:StatisticalInformation)|epo:ReceivedNONEEATenderLots (from epo:StatisticalInformation)
|epo:SubmissionStatisticalInformation|epo:hasReceivedParticipationRequests (from epo:StatisticalInformation)|epo:ReceivedParticipationRequests (from epo:StatisticalInformation)
|epo:SubmissionStatisticalInformation|epo:hasReceivedSMETenders (from epo:StatisticalInformation)|epo:ReceivedSMETenderLots (from epo:StatisticalInformation)
|epo:SubmissionStatisticalInformation|epo:hasReceivedSmallTenders (from epo:StatisticalInformation)|epo:ReceivedSmallTenderLots (from epo:StatisticalInformation)
|epo:SubmissionStatisticalInformation|epo:hasReceivedTenders (from epo:StatisticalInformation)|epo:ReceivedTenderLots (from epo:StatisticalInformation)
|epo:SubmissionStatisticalInformation|epo:hasEstimatedTotalSubcontracts (from epo:StatisticalInformation)|epo:TotalValueSubcontracted (from epo:StatisticalInformation)
|epo:SubmissionStatisticalInformation|epo:hasUnverifiedTenders (from epo:StatisticalInformation)|epo:UnverifiedTenderLots (from epo:StatisticalInformation)
|epo:SubcontractingEstimate|epo:hasDescription (from epo:Subcontract)|
|epo:SubcontractingEstimate|epo:hasEstimatedPercentage (from epo:Subcontract)|
|epo:SubcontractingEstimate|epo:hasSubjectMatter (from epo:Subcontract)|
|epo:RegulatoryFrameworkInformation||epo:RegulatoryFrameworkProvider
|===

|===
|*class*|*added property*|*deleted property*

|epo:LotAwardOutcome|epo:providesAwardedEstimatedValue -> epo:MonetaryValue|
|epo:LotAwardOutcome|epo:isAdoptedByBuyer -> epo:Buyer|
|epo:LotAwardOutcome|epo:hasAwardStatus -> at-voc:winner-selection-status|
|epo:LotAwardOutcome|epo:providesAwardedValue -> epo:MonetaryValue|
|epo:LotAwardOutcome|epo:providesFrameworkAgreementMaximumValue -> epo:MonetaryValue|
|epo:LotAwardOutcome|epo:providesFrameworkAgreementEstimatedValue -> epo:MonetaryValue|
|epo:LotAwardOutcome|epo:describesLot -> epo:Lot|
|epo:LotAwardOutcome|epo:comprisesTenderAwardOutcome -> epo:TenderAwardOutcome|
|epo:LotAwardOutcome|epo:hasNonAwardJustification -> at-voc:non-award-justification|
|epo:LotAwardOutcome|epo:considersEvaluationResult -> epo:TenderEvaluationResult|
|epo:LotGroupAwardInformation|epo:hasGroupFrameworkAgreementAwardedValue -> epo:MonetaryValue|
|epo:LotGroupAwardInformation|epo:describesLotGroup -> epo:LotGroup|
|epo:NoticeAwardInformation|epo:hasTotalFrameworkAgreementAwardedValue -> epo:MonetaryValue|
|epo:NoticeAwardInformation|epo:describesResultNotice -> epo:ResultNotice|
|epo:NoticeAwardInformation|epo:indicatesCancelledLotToBeRelaunched -> epo:Lot|
|epo:NoticeAwardInformation|epo:hasTotalContractAwardedValue -> epo:MonetaryValue|
|epo:TenderAwardOutcome|epo:describesTender -> epo:Tender|
|epo:TenderAwardOutcome|epo:isAwardedToWinner -> epo:Winner|
|epo:ContractLotCompletionInformation|epo:refersToContract -> epo:Contract|
|epo:ContractLotCompletionInformation|epo:hasPenaltyValue -> epo:MonetaryValue|
|epo:ContractLotCompletionInformation|epo:describesLotCompletion -> epo:Lot|
|epo:ContractLotCompletionInformation|epo:hasPaymentValue -> epo:MonetaryValue|
|epo:ReviewDecisionInformation|generalisation -> epo:ReviewInformation|
|epo:ReviewDecisionInformation|epo:reviewDecisionType -> at-voc:decision-type|
|epo:ReviewInformation|epo:hasID -> epo:Identifier|
|epo:ReviewInformation|epo:previousReview -> epo:ReviewInformation|
|epo:ReviewInformation|epo:hasRemedyValue -> epo:MonetaryValue|
|epo:ReviewInformation|epo:hasIrregularityType -> at-voc:irregularity-type|
|epo:ReviewInformation|epo:reviewRemedyType -> at-voc:review-remedy-type|
|epo:ReviewRequestInformation|generalisation -> epo:ReviewInformation|
|epo:ReviewRequestInformation|epo:hasReviewRequestFee -> epo:MonetaryValue|
|epo:ReviewIrregularitySummary|epo:hasIrregularityType -> at-voc:irregularity-type|
|epo:ReviewRequestSummary|epo:hasReviewIrregularitySummary -> epo:ReviewIrregularitySummary|
|epo:ReviewRequestSummary|epo:concernsReviewSummaryForLot -> epo:Lot|
|epo:SubmissionStatisticalInformation|epo:hasHighestReceivedTenderValue -> epo:MonetaryValue|
|epo:SubmissionStatisticalInformation|epo:hasReceivedSubmissionType -> at-voc:received-submission-type|
|epo:SubmissionStatisticalInformation|epo:hasLowestReceivedTenderValue -> epo:MonetaryValue|
|epo:SubmissionStatisticalInformation|epo:concernsSubmissionsForLot -> epo:Lot|
|epo:SubcontractingEstimate|epo:hasSubcontractingEstimatedValue -> epo:MonetaryValue (form epo:Subcontract)|
|epo:RegulatoryFrameworkInformation|epo:hasRegulatoryFrameworkType -> epo:regulatory-framework-type|
|epo:ElementChangeSpecification|generalisation -> epo:ElementDescription|
|===

==== Notice description

|===
|*class*|*added attributes*|*deleted attributes*

|epo:ElementChangeSpecification|po:hasProcurementDocumentChangeDate|epo:DateTime
|epo:ElementChangeSpecification|epo:hasChangeDescription|epo:Description
|epo:ElementChangeSpecification|epo:hasChangeReasonDescription|epo:Reason
|epo:ElementChangeSpecification|epo:hasElementReference|
|epo:ElementChangeSpecification|epo:hasPreviousVersionOfElementReference|
|epo:ElementChangeSpecification||epo:ChangeReason
|epo:ElementConfidentialitySpecification|epo:hasAccessibilityDate|
|epo:ElementConfidentialitySpecification|epo:hasClassReference|
|epo:ElementConfidentialitySpecification|epo:hasConfidentialityJustification|
|epo:ElementConfidentialitySpecification|epo:hasPropertyReference|
|epo:ElementModificationSpecification|epo:hasModificationDescription (from epo:ContratModificationNotice)|epo:Description (from epo:ContractModificationNotice)
|epo:ElementModificationSpecification|epo:hasModificationReasonDescription (from epo:ContratModificationNotice)|epo:Justification (from epo:ContratModificationNotice)
|epo:ElementModificationSpecification|epo:hasElementReference|
|epo:PublicationProvision||epo:AvailabilityDate
|epo:PublicationProvision||epo:NonPublicationJustificationDescription
|epo:PublicationProvision||epo:NonPublicationJustification
|===

|===
|*class*|*added property*|*deleted property*

|epo:ElementChangeSpecification|epo:hasChangeJustification -> at-voc:change-corrig-justification|epo:hasChangeReason -> at-voc:change-corrig-justification
|epo:ElementChangeSpecification||epo:refersToADifferent -> epo:Document
|epo:ElementChangeSpecification||epo:hasChangeElement -> epo:ResourceElement
|epo:ContractModification|generalisation -> epo:NoticeDescription|
|epo:ContractModification|epo:hasElementModificationSpecification -> epo:ElementModificationSpecification|
|epo:ContractModification|epo:refersToOriginalNotice -> epo:Notice|
|epo:ElementConfidentialitySpecification|generalisation -> epo:ElementDescription|
|epo:ElementConfidentialitySpecification|epo:hasNonPublicationJustification -> at-voc:non-publication-justification|
|epo:ElementModificationSpecification|epo:hasModificationJustification -> at-voc:modification-justification (from epo:ContratModificationNotice)|epo:hasContractModficationJustification -> at-voc:modification-justification (from epo:ContratModificationNotice)
|epo:ElementModificationSpecification|generalisation -> epo:ElementDescription|
|epo:NoticeChange|epo:hasElementChangeSpecification -> epo:ElementChangeSpecification|
|epo:NoticeChange|generalisation -> epo:NoticeDescription|
|epo:NoticeChange|epo:refersToPreviousNotice -> epo:Notice|
|epo:NoticeDescription|epo:describesNotice -> epo:Notice|
|epo:NoticeDescription|epo:hasElementDescription -> epo:ElementDescription|
|epo:PublicationProvision|generalisation -> epo:NoticeDescription|
|epo:PublicationProvision|epo:hasFieldConfidentiality -> epo:ElementConfidentialitySpecification|
|epo:PublicationProvision||epo:hasNonPublicationJustification -> at-voc:non-publication-justification
|epo:PublicationProvision||epo:hasNonPublishedElement -> epo:ResourceElement
|===

==== Dimension package

|===
|*class*|*added attributes*|*deleted attributes*

|epo:Duration|time:numericDuration|
|epo:Period|epo:hasBeginning|epo:StartDate
|epo:Period|epo:hasEnd|epo:EndTime
|epo:MonetaryValue|epo:hasCurrencyCodeListAgencyID|epo:UnitCodeListAgencyID (from epo:Amount)
|epo:MonetaryValue|epo:hasCurrencyCodeListAgencyName|epo:UnitCodeListAgencyName (from epo:Amount)
|epo:MonetaryValue|epo:hasCurrencyCodeListID|epo:UnitCodeListID (from epo:Amount)
|epo:MonetaryValue||epo:MaximumAmount (from epo:Value)
|epo:MonetaryValue||epo:MinimumAmount (from epo:Value)
|epo:MonetaryValue||epo:OverallAmount
|epo:MonetaryValue||epo:VATIncludedIndicator (from epo:Amount)
|epo:MonetaryValue||epo:VATPercentage (from epo:Amount)
|===

|===
|*class*|*added property*|*deleted property*

|epo:Duration|time:unitType -> time:TemporalUnit|
|epo:Period|epo:hasTimePeriod -> at-voc:timeperiod|epo:hasTimePeriods -> at-voc:timeperiod
|epo:Quantity|epo:hasUnitCode -> at-voc:measurement-unit|
|epo:MonetaryValue|epo:hasCurrency -> at-voc:currency (from epo:Amount)|
|===