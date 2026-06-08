<?
if (!defined("B_PROLOG_INCLUDED") || B_PROLOG_INCLUDED !== true) {
    die();
}

class SelectSiteStep extends CWizardStep
{
    public function InitStep()
    {
        $wizard =& $this->GetWizard();
        $wizard->solutionName = "simai.example";
        LocalRedirect("/simai/wizard/master/simai.example/");
    }
}
